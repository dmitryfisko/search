from urllib.parse import urlparse, urlunparse
from urllib.parse import urlsplit, urlunsplit, parse_qsl
from urllib.parse import urlencode
import re


class UrlNorm:
    MAX_IP = 0xffffffff

    class InvalidUrl(Exception):
        pass

    def __init__(self):
        self._collapse = re.compile('([^/]+/\.\./?|/\./|//|/\.$|/\.\.$)')
        self._server_authority = re.compile('^(?:([^@]+)@)?([^:\[\]]+|\[[a-fA-F0-9:\.]+\])(?::(.*?))?$')
        self._default_port = {'http': '80',
                              'itms': '80',
                              'ws': '80',
                              'https': '443',
                              'wss': '443',
                              'gopher': '70',
                              'news': '119',
                              'snews': '563',
                              'nntp': '119',
                              'snntp': '563',
                              'ftp': '21',
                              'telnet': '23',
                              'prospero': '191',
                              }
        self._relative_schemes = ['http',
                                  'https',
                                  'ws',
                                  'wss',
                                  'itms',
                                  'news',
                                  'snews',
                                  'nntp',
                                  'snntp',
                                  'ftp',
                                  'file',
                                  ''
                                  ]

        self.params_unsafe_list = ' ?=+%#;'
        self.qs_unsafe_list = ' ?&=+%#'
        self.fragment_unsafe_list = ' +%#'
        self.path_unsafe_list = '/?;%+#'
        self._hextochr = dict(('%02x' % i, chr(i)) for i in range(256))
        self._hextochr.update(('%02X' % i, chr(i)) for i in range(256))

    def canonize(self, url):
        split = urlsplit(self._norm(url))
        path = split[2].split(' ')[0]

        while path.startswith('/..'):
            path = path[3:]

        while path.endswith('%20'):
            path = path[:-3]

        qs = urlencode(sorted(parse_qsl(split.query)))
        return urlunsplit((split.scheme, split.netloc, path, qs, ''))

    def _unquote_path(self, s):
        return self._unquote_safe(s, self.path_unsafe_list)

    def _unquote_params(self, s):
        return self._unquote_safe(s, self.params_unsafe_list)

    def _unquote_qs(self, s):
        return self._unquote_safe(s, self.qs_unsafe_list)

    def _unquote_fragment(self, s):
        return self._unquote_safe(s, self.fragment_unsafe_list)

    def _unquote_safe(self, s, unsafe_list):
        """unquote percent escaped string except for percent escape sequences that are in unsafe_list"""
        # note: this build utf8 raw strings ,then does a .decode('utf8') at the end.
        # as a result it's doing .encode('utf8') on each block of the string as it's processed.
        res = s.split('%')
        for i in range(1, len(res)):
            item = res[i]
            try:
                raw_chr = self._hextochr[item[:2]]
                if raw_chr in unsafe_list or ord(raw_chr) < 20:
                    # leave it unescaped (but uppercase the percent escape)
                    res[i] = '%' + item[:2].upper() + item[2:]
                else:
                    res[i] = raw_chr + item[2:]
            except KeyError:
                res[i] = '%' + item
            except UnicodeDecodeError:
                # note: i'm not sure what this does
                res[i] = chr(int(item[:2], 16)) + item[2:]
        o = "".join(res)
        return o

    def _norm(self, url):
        """given a string URL, return its normalized/unicode form"""
        url_tuple = urlparse(url)
        normalized_tuple = self._norm_tuple(*url_tuple)
        return urlunparse(normalized_tuple)

    def _norm_tuple(self, scheme, authority, path, parameters, query, fragment):
        """given individual url components, return its normalized form"""
        scheme = scheme.lower()
        if not scheme:
            raise self.InvalidUrl('missing URL scheme')
        authority = self._norm_netloc(scheme, authority)
        if not authority:
            raise self.InvalidUrl('missing netloc')
        path = self._norm_path(scheme, path)
        parameters = self._unquote_params(parameters)
        query = self._unquote_qs(query)
        fragment = self._unquote_fragment(fragment)
        return scheme, authority, path, parameters, query, fragment

    def _norm_path(self, scheme, path):
        if scheme in self._relative_schemes:
            last_path = path
            while 1:
                path = self._collapse.sub('/', path, 1)
                if last_path == path:
                    break
                last_path = path
        path = self._unquote_path(path)
        if not path:
            return '/'
        return path

    def _int2ip(self, ipnum):
        assert isinstance(ipnum, int)
        if self.MAX_IP < ipnum or ipnum < 0:
            raise TypeError("expected int between 0 and %d inclusive" % self.MAX_IP)
        ip1 = ipnum >> 24
        ip2 = ipnum >> 16 & 0xFF
        ip3 = ipnum >> 8 & 0xFF
        ip4 = ipnum & 0xFF
        return "%d.%d.%d.%d" % (ip1, ip2, ip3, ip4)

    def _norm_netloc(self, scheme, netloc):
        if not netloc:
            return netloc
        match = self._server_authority.match(netloc)
        if not match:
            raise self.InvalidUrl('no host in netloc %r' % netloc)

        userinfo, host, port = match.groups()
        # catch a few common errors:
        if host.isdigit():
            try:
                host = self._int2ip(int(host))
            except TypeError:
                raise self.InvalidUrl('host %r does not escape to a valid ip' % host)
        if host[-1] == '.':
            host = host[:-1]

        # bracket check is for ipv6 hosts
        if '.' not in host and not (host[0] == '[' and host[-1] == ']'):
            raise self.InvalidUrl('host %r is not valid' % host)

        authority = host.lower()
        if 'xn--' in authority:
            subdomains = [self._idn(subdomain) for subdomain in authority.split('.')]
            authority = '.'.join(subdomains)

        if userinfo:
            authority = "%s@%s" % (userinfo, authority)
        if port and port != self._default_port.get(scheme, None):
            authority = "%s:%s" % (authority, port)
        return authority

    def _idn(self, subdomain):
        if subdomain.startswith('xn--'):
            try:
                subdomain = subdomain.decode('idna')
            except UnicodeError:
                raise self.InvalidUrl('Error converting subdomain %r to IDN' % subdomain)
        return subdomain

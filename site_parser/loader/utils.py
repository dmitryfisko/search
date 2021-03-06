import logging
import time
from _socket import timeout
from http.client import HTTPException
from multiprocessing import RLock
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from nltk import defaultdict
from reppy.cache import RobotsCache

from site_parser.loader.urlnorm import UrlNorm
from site_parser.models import WebSite, Page, settings

UNLIMITED_DEPTH = 10000

LOGGING_ENABLED = False
logger = logging.getLogger(__name__)


class QueueItem:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth


class Coordinator:
    def __init__(self, depth=UNLIMITED_DEPTH):
        self._prev_time = 0
        self.lock = RLock()
        self.depth_limit = depth

    def next_wait_time(self):
        with self.lock:
            curr_time = time.time()
            passed_time = curr_time - self._prev_time

            if passed_time >= settings.REQUEST_MIN_DELAY:
                self._prev_time = curr_time
                return 0
            else:
                return settings.REQUEST_MIN_DELAY - passed_time


class UrlManager:
    USER_AGENT = 'SiteParser'

    def __init__(self, robots_url=None):
        if robots_url:
            robots = RobotsCache()
            self._rules = robots.fetch(robots_url)
            self.is_use_robots = True
        else:
            self.is_use_robots = False

        self._url_norm = UrlNorm()
        self.counter = 0
        self.urls = dict()
        self.connections = defaultdict(set)
        self._lock = RLock()

    def __contains__(self, url):
        url_was = url in self.urls
        if self.is_use_robots:
            url_allowed = self._rules.allowed(url, self.USER_AGENT)
            return url_was or not url_allowed
        else:
            return url_was

    def canonize(self, url):
        return self._url_norm.canonize(url)

    def add(self, url):
        ind = self.urls.get(url)
        if not ind:
            with self._lock:
                self.counter += 1
                ind = self.counter
            self.urls[url] = ind
        return ind

    def add_canonize(self, url):
        url = self.canonize(url)
        ind = self.add(url)
        return ind, url

    def connect_urls(self, url1, url2):
        ind1 = self.add(url1)
        ind2 = self.add(url2)

        self.connections[ind1].add(ind2)


class Utils:
    @staticmethod
    def get_or_create_page_model(url):
        page_exist = Page.objects.filter(url=url).exists()
        if not page_exist:
            page = Page(url=url)
            page.save()
        else:
            page = Page.objects.get(url=url)

        return page

    @staticmethod
    def get_or_create_site_model(domain):
        site_exist = WebSite.objects.filter(domain=domain).exists()
        if not site_exist:
            site = WebSite(domain=domain)
            site.save()
        else:
            site = WebSite.objects.get(domain=domain)

        return site

    @staticmethod
    def clean_text(soup):
        [s.decompose() for s in soup(['script', 'style'])]
        return ' '.join(soup.stripped_strings)

    @staticmethod
    def download_url(url, request_timeout):
        try:
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
            response = urlopen(request, timeout=request_timeout)
            return response.read().decode('utf8')
        except HTTPError:
            error = 'url request HTTPException'
        except HTTPException:
            error = 'url request HTTPException'
        except timeout:
            error = 'url request HTTPException'
        except URLError:
            error = 'url request HTTPException'
        except Exception:
            error = 'url request unhandled request error'

        if LOGGING_ENABLED:
            logger.error(error)

        return None

    @staticmethod
    def extract_domain(url):
        domain = urlparse(url).netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

    @staticmethod
    def filter_links_from_domain(url_manager, links, domain):
        filtered_hrefs = []
        external_hrefs = []
        for link in links:
            url = link.get('href')
            if not url:
                continue

            try:
                url = url_manager.canonize(url)
            except UrlNorm.InvalidUrl:
                continue

            url = url_manager.canonize(url)
            if Utils.extract_domain(url) == domain:
                filtered_hrefs.append(url)
            else:
                external_hrefs.append(url)
        return filtered_hrefs, external_hrefs

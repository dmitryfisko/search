import urllib
from urllib.error import URLError
from urllib.request import urlopen, Request

import re
from celery.signals import worker_process_init


@worker_process_init.connect
def fix_multiprocessing(**kwargs):
    from multiprocessing import current_process
    try:
        current_process()._config
    except AttributeError:
        current_process()._config = {'semprefix': '/mp'}


def fix_schema(url):
    if not re.match('^http(s?)://', url):
        url = 'http://' + url
    return url + ('/' if url[-1] != '/' else '')


def convert_to_int(num):
    try:
        num = int(num)
        if num < 0:
            return None
        else:
            return num
    except TypeError:
        return None
    except ValueError:
        return None


def check_url(url):
    request = Request(url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')

    try:
        urlopen(request, timeout=5)
    except URLError as _:
        return False
    else:
        return True

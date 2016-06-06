from __future__ import absolute_import

from celery import shared_task

from site_parser.loader.loader import SiteLoader
from site_parser.loader.utils import Coordinator
from site_parser.utils import fix_multiprocessing, check_url, fix_schema


@shared_task
def start_parser(url, depth):
    # command to start celery worker
    # /usr/bin/python3.5 manage.py celery -A search worker -l info --concurrency=10
    fix_multiprocessing()

    url = fix_schema(url)
    if check_url(url):
        coord = Coordinator()
        loader = SiteLoader(coord)
        loader.start(url)

        return 'url parsed: %s' % url
    else:
        return 'bad url'

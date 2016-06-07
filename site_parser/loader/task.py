import logging
import threading
import time

from bs4 import BeautifulSoup

from site_parser.loader.utils import Utils, QueueItem


class UrlLoaderTask(threading.Thread):
    REQUEST_TIMEOUT = 5

    def __init__(self, que, url_manager, site, coord):
        threading.Thread.__init__(self)
        self._queue = que
        self._coord = coord
        self._site = site
        self._url_manager = url_manager
        self._is_active_job = False

    def is_active_job(self):
        return self._is_active_job

    def _is_url_need_parsing(self, depth):
        if depth > self._coord.depth_limit:
            return False
        else:
            return True

    def _process_new_links(self, soup, depth):
        if depth + 1 > self._coord.depth_limit:
            return

        domain = self._site.domain
        hrefs = Utils.filter_links_from_domain(soup.find_all('a'), domain)
        for href in hrefs:
            if href not in self._url_manager:
                self._url_manager.add(href)
                queue_url = QueueItem(href, depth=depth + 1)
                self._queue.put(queue_url)

    def run(self):
        logger = logging.getLogger('site_parser')

        while True:
            queue_item = self._queue.get()
            self._is_active_job = True
            if isinstance(queue_item, str) and queue_item == 'quit':
                self._is_active_job = False
                break

            wait = self._coord.next_wait_time()
            while wait != 0:
                time.sleep(wait)
                wait = self._coord.next_wait_time()

            url, depth = queue_item.url, queue_item.depth
            logger.info('url parsing: %s' % url)

            raw_html = Utils.download_url(url, self.REQUEST_TIMEOUT)
            if raw_html:
                soup = BeautifulSoup(raw_html, 'lxml')
                self._process_new_links(soup, depth)

                page_model = Utils.get_or_create_page_model(url)
                page_model.text = Utils.clean_text(soup)
                page_model.title = soup.title.string
                page_model.save()

            logger.info('url parsed: %s' % url)
            self._is_active_job = False

        logging.info('PhotoTask thread close')

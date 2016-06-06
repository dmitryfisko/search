import logging
import threading
import time
from _socket import timeout
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup

from site_parser.loader.utils import Tokenizer, Utils, QueueItem


class UrlLoaderTask(threading.Thread):
    REQUEST_TIMEOUT = 5

    def __init__(self, que, words_counter, site, coord):
        threading.Thread.__init__(self)
        self._queue = que
        self._coord = coord
        self._site = site
        self._site_words_counter = words_counter
        self._is_active_job = False

    def is_active_job(self):
        return self._is_active_job

    def _add_words_to_site_words_counter(self, tokens):
        self._site_words_counter = {**self._site_words_counter, **tokens}

    def _is_url_need_parsing(self, depth):
        if depth > self._coord.depth_limit:
            return False
        else:
            return True

    def _process_new_links(self, url_model, soup, depth):
        domain = self._site.domain
        parse_iteration = self._site.parse_iteration
        hrefs = Utils.filter_links_from_domain(soup.find_all('a'), domain)
        for href in hrefs:
            href_model = Utils.get_or_create_url_model(href)
            url_model.urls_to.add(href_model)

            with self._coord.lock:
                if href_model.parse_iteration < parse_iteration:
                    href_model.parse_iteration = parse_iteration
                    href_model.save()
                    queue_url = QueueItem(href, depth=depth + 1)
                    self._queue.put(queue_url)

    def _process_tokens(self, tokens, url_model):
        self._add_words_to_site_words_counter(tokens)
        url_model.clear_dict()
        url_model.set_words_frequency(tokens)

        for token in tokens.keys():
            word_model = Utils.get_or_create_word_model(token)
            word_model.urls.add(url_model)

    def run(self):
        tokenizer = Tokenizer()

        while True:
            url, depth = self._queue.get()
            self._is_active_job = True
            if isinstance(url, str) and url == 'quit':
                self._is_active_job = False
                break

            if not self._is_url_need_parsing(depth):
                continue

            wait = self._coord.next_wait_time()
            while wait != 0:
                time.sleep(wait)
                wait = self._coord.next_wait_time()

            response = Utils.send_request(url, self.REQUEST_TIMEOUT)
            if response:
                raw_html = response.read().decode('utf8')
                soup = BeautifulSoup(raw_html)
                raw_text = soup.get_text()
                tokens = tokenizer.tokenize(raw_text)

                url_model = Utils.get_or_create_url_model(url)
                self._process_new_links(soup, url_model, depth)
                self._process_tokens(tokens, url_model)
                url_model.raw_text = raw_text
                url_model.save()

            self._is_active_job = False

        logging.info('PhotoTask thread close')

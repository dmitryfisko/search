import logging
import threading
import time
from _socket import timeout
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from site_parser.loader.utils import Tokenizer, filter_links_from_domain, get_or_create_url_model, \
    get_or_create_word_model


class UrlLoaderTask(threading.Thread):
    URL_REQUEST_TIMEOUT = 5

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
        if depth > self._coord.max_depth:
            return False
        else:
            return True

    def _process_new_links(self, url_model, soup):
        domain = self._site.domain
        hrefs = filter_links_from_domain(soup.find_all('a'), domain)
        for href in hrefs:
            href_model = get_or_create_url_model(href)
            url_model.urls_to.add(href_model)

    def _process_tokens(self, tokens, url_model):
        self._add_words_to_site_words_counter(tokens)
        url_model.clear_dict()
        url_model.set_words_frequency(tokens)

        for token in tokens.keys():
            word_model = get_or_create_word_model(token)
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

            try:
                response = urlopen(url, timeout=self.URL_REQUEST_TIMEOUT)
                raw_html = response.read().decode('utf8')
                soup = BeautifulSoup(raw_html)
                raw_text = soup.get_text()
                tokens = tokenizer.tokenize(raw_text)

                url_model = get_or_create_url_model(url)
                self._process_new_links(soup, url_model)
                self._process_tokens(tokens, url_model)

            except ValueError:
                # logging.error(u"Photos request failed "
                #               u"to parse response of url: {}".format(request_url))
                users_photos = []
            except HTTPError:
                # logging.error("Photos request HTTPException")
                users_photos = []
            except HTTPException:
                # logging.error("Photos request HTTPException")
                users_photos = []
            except timeout:
                # logging.error("Photos request timeout")
                users_photos = []
            except URLError:
                # logging.error("Photos request URLError")
                users_photos = []
            except Exception:
                # logging.exception("Photos request unknown exception")
                users_photos = []

            url_model.parse_iteration = self._coord.parse_iteration
            self._is_active_job = False

        logging.info('PhotoTask thread close')
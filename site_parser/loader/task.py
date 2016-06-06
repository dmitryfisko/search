import json
import logging
import threading
import time
from _socket import timeout
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

from site_parser.loader.utils import Tokenizer


class UrlLoaderTask(threading.Thread):
    URL_REQUEST_TIMEOUT = 5

    def __init__(self, que, words_counter, coord):
        threading.Thread.__init__(self)
        self._queue = que
        self._coord = coord
        self._site_counter = words_counter
        self._is_active_job = False

    def is_active_job(self):
        return self._is_active_job

    def _add_in_site_counter(self, tokens):
        self._site_counter = {**self._site_counter, **tokens}

    def run(self):
        tokenizer = Tokenizer()

        while True:
            url, depth = self._queue.get()
            self._is_active_job = True
            if isinstance(url, str) and url == 'quit':
                self._is_active_job = False
                break

            if depth > self._coord.max_depth:
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
                self._add_in_site_counter(tokens)


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

            self._is_active_job = False

        logging.info('PhotoTask thread close')
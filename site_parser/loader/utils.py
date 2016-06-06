import logging
import string
from _socket import timeout
from collections import Counter
from http.client import HTTPException
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import pymorphy2
from multiprocessing import RLock

import time
from nltk import word_tokenize, WordNetLemmatizer

from site_parser.models import Url, Site, Word

UNLIMITED_DEPTH = 10000

LOGGING_ENABLED = False
logger = logging.getLogger(__name__)


class QueueItem:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth


class Coordinator:
    def __init__(self, depth=UNLIMITED_DEPTH, requests_delay=0.5):
        self._prev_time = 0
        self._requests_delay = requests_delay
        self.lock = RLock()
        self.depth_limit = depth

    def next_wait_time(self):
        with self.lock:
            curr_time = time.time()
            passed_time = curr_time - self._prev_time

            if passed_time >= self._requests_delay:
                self._prev_time = curr_time
                return 0
            else:
                return self._requests_delay - passed_time


class Tokenizer:
    def __init__(self):
        self._ru_lemma = pymorphy2.MorphAnalyzer()
        self._en_lemma = WordNetLemmatizer()

    @staticmethod
    def _strip_word(word):
        return word.strip(string.punctuation)

    def _lemmatize_word(self, word):
        word = self._ru_lemma.parse(word)[0].normal_form
        word = self._en_lemma.lemmatize(word)
        return word

    def tokenize(self, raw_text):
        raw_tokens = word_tokenize(raw_text.lower())
        tokens = []
        for token in raw_tokens:
            token = self._strip_word(token)
            if token:
                token = self._lemmatize_word(token)
                tokens.append(token)

        return Counter(tokens)


class Utils:
    @staticmethod
    def get_or_create_url_model(path):
        url_exist = Url.objects.filter(path=path).exists()
        if not url_exist:
            url = Url(path=path)
            url.save()
        else:
            url = Url.objects.get(path=path)

        return url

    @staticmethod
    def get_or_create_site_model(domain):
        site_exist = Site.objects.filter(domain=domain).exists()
        if not site_exist:
            site = Site(domain=domain)
            site.save()
        else:
            site = Site.objects.get(domain=domain)

        return site

    @staticmethod
    def get_or_create_word_model(value):
        word_exist = Word.objects.filter(value=value).exists()
        if not word_exist:
            word = Word(value=value)
            word.save()
        else:
            word = Word.objects.get(value=value)

        return word

    @staticmethod
    def clean_text(soup):
        [s.decompose() for s in soup(['script', 'style'])]
        return ' '.join(soup.stripped_strings)

    @staticmethod
    def send_request(url, request_timeout):
        try:
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
            response = urlopen(request, timeout=request_timeout)
            return response
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
        return urlparse(url).netloc

    @staticmethod
    def filter_links_from_domain(links, domain):
        filtered_hrefs = []
        for link in links:
            url = link.get('href')
            if Utils.extract_domain(url) == domain:
                filtered_hrefs.append(url)
        return filtered_hrefs

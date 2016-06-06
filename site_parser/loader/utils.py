import string
from collections import Counter
from urllib.parse import urlparse

import pymorphy2

from nltk import word_tokenize, WordNetLemmatizer

from site_parser.models import Url, Site, Word

UNLIMITED_DEPTH = 10000


class QueueUrl:
    def __init__(self, url, depth):
        self.url = url
        self.depth = depth


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


def get_or_create_url_model(path):
    url_exist = Url.objects.filter(path=path).exists()
    if not url_exist:
        url = Url(path)
        url.save()
    else:
        url = Url.objects.get(path=path)

    return url


def get_or_create_site_model(domain):
    site_exist = Site.objects.filter(domain=domain).exists()
    if not site_exist:
        site = Site(domain=domain)
        site.save()
    else:
        site = Site.objects.get(domain=domain)

    return site


def get_or_create_word_model(value):
    word_exist = Word.objects.filter(value=value).exists()
    if not word_exist:
        word = Word(value=value)
        word.save()
    else:
        word = Word.objects.get(value=value)

    return word


def extract_domain(url):
    return urlparse(url).netloc


def filter_links_from_domain(links, domain):
    filtered_hrefs = []
    for link in links:
        url = link.get('href')
        if extract_domain(url) == domain:
            filtered_hrefs.append(url)

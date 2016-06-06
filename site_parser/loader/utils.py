import string
from collections import Counter

import pymorphy2

from nltk import word_tokenize, WordNetLemmatizer


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

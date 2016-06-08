import json
import string

import ahocorasick
from nltk import word_tokenize

from site_parser.loader.utils import Utils
from site_parser.utils import fix_schema


class Snippet:
    SNIPPET_MAX_LEN = 200
    SNIPPET_MIN_LEN = 100
    MAX_SENTENCE_EXPAND_ITERATIONS = 7

    def __init__(self, query):
        self._automaton = ahocorasick.Automaton()
        tokens = Snippet.tokenize(query)
        for i in range(len(tokens)):
            query_part = ''
            for token in tokens[i:]:
                query_part += token
                self._automaton.add_word(query_part, len(query_part))
                query_part += ' '
        self._automaton.make_automaton()

    @staticmethod
    def _strip_word(word):
        return word.strip(string.punctuation)

    @staticmethod
    def normalize_snippet(snippet):
        snippet = ' '.join(snippet.split())
        tabulation = '\t\n\r'
        ''.join([ch for ch in snippet if ch not in tabulation])
        return snippet.strip()

    @staticmethod
    def tokenize(raw_text):
        raw_tokens = word_tokenize(raw_text.lower())
        tokens = []
        for token in raw_tokens:
            token = Snippet._strip_word(token)
            if token:
                tokens.append(token)

        return tokens

    def make_snippet(self, text):
        entries = []
        for entry in self._automaton.iter(text.lower()):
            entries.append(entry)
        longest_entry = max(entries, key=lambda x: x[1])

        left_side = longest_entry[0] - longest_entry[1] + 1
        right_side = longest_entry[0]

        is_right = False
        iteration = 0
        while True:
            if is_right:
                start = right_side + 1
                point_ind = start + text[start:].find('.')
                if point_ind - left_side + 1 <= Snippet.SNIPPET_MAX_LEN:
                    right_side = point_ind
            else:
                point_ind = text[:left_side].rfind('.')
                if right_side - point_ind + 1 <= Snippet.SNIPPET_MAX_LEN:
                    left_side = point_ind

            iteration += 1
            if iteration >= Snippet.MAX_SENTENCE_EXPAND_ITERATIONS:
                break
            is_right = not is_right

        snippet = text[left_side: right_side + 1]
        if len(snippet) < self.SNIPPET_MIN_LEN:
            snippet = text[left_side:left_side + self.SNIPPET_MIN_LEN]

        if snippet[0] == '.':
            snippet = snippet[1:]

        if snippet[-1] != '.':
            snippet += '...'

        return Snippet.normalize_snippet(snippet)


class ApiUtils:
    @staticmethod
    def extract_query_params(query):
        filtered_tokens = []
        params = {}
        tokens = query.split(' ')
        for token in tokens:
            colon_ind = token.find(':')
            if colon_ind != -1:
                special = token[:colon_ind]
                value = token[colon_ind + 1:]
                if special == 'site':
                    site = fix_schema(value)
                    domain = Utils.extract_domain(site)
                    params[special] = domain
                elif special == 'lang' and len(value) == 2:
                    params[special] = value
            else:
                filtered_tokens.append(token)
        return ' '.join(filtered_tokens), params

    @staticmethod
    def parse_urls_file(file):
        try:
            content = json.load(file)
        except:
            return None
        return ApiUtils.parse_urls_data(content)

    @staticmethod
    def parse_urls_data(content):
        depth = content.get('depth')
        urls = content.get('urls')
        if urls and not all(isinstance(url, str) for url in urls):
            urls = None
        return depth, urls

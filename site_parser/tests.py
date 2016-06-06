from django.test import TestCase

from site_parser.models import Url


class QuestionMethodTests(TestCase):

    def test_save_dictionary_to_url_model(self):
        tokens = {'I': 3, 'am': 7}
        url = 'http://www.example.com/'
        raw_text = 'dsfsdfsdfsdf'
        url = Url(url=url, raw_text=raw_text)
        url.set_words_frequency(tokens)
        url.save()

        self.assertTrue(url['I'] == 3)
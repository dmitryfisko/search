from django.contrib.postgres import fields
from django.db import models

from site_parser.model_dict import Dictionary


class Url(Dictionary):
    url = models.CharField(max_length=40, primary_key=True)
    urls_to = models.ManyToManyField('self')
    raw_text = models.TextField()

    def __init__(self, *args, **kwargs):
        super().__init__(self.url, *args, **kwargs)

    def set_words_frequency(self, counter):
        for key, value in counter.items():
            self[key] = value


class Site(Dictionary):
    domain = models.CharField(max_length=100, primary_key=True)
    urls = models.ManyToManyField(Url)

    def __init__(self, *args, **kwargs):
        super().__init__(self.domain, *args, **kwargs)

    def set_words_frequency(self, counter):
        for key, value in counter.items():
            self[key] = value


class Word(models.Model):
    value = models.CharField(max_length=30, primary_key=True)
    urls = models.ManyToManyField(Url)

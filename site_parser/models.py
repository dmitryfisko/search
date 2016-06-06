from django.contrib.postgres import fields
from django.db import models

from site_parser.model_dict import Dictionary


class Url(Dictionary):
    path = models.CharField(max_length=40, primary_key=True)
    urls_to = models.ManyToManyField('self')
    raw_text = models.TextField()
    parse_iteration = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(self.url, *args, **kwargs)


class Site(Dictionary):
    domain = models.CharField(max_length=100, primary_key=True)
    urls = models.ManyToManyField(Url)
    iteration_num = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(self.domain, *args, **kwargs)


class Word(models.Model):
    value = models.CharField(max_length=30, primary_key=True)
    urls = models.ManyToManyField(Url)

from django.contrib.postgres import fields
from django.db import models

from site_parser.model_dict import Dictionary

class Url(Dictionary):
    path = models.CharField(max_length=40, primary_key=True)
    urls_to = models.ManyToManyField('self')
    text = models.TextField()
    parse_iteration = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        path = kwargs['path'] if kwargs else args[0]
        super().__init__(path, *args, **kwargs)


class Site(Dictionary):
    domain = models.CharField(max_length=100, primary_key=True)
    urls = models.ManyToManyField(Url)
    parse_iteration = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        domain = kwargs['domain'] if kwargs else args[2]
        super().__init__(domain, *args, **kwargs)


class Word(models.Model):
    value = models.CharField(max_length=30, primary_key=True)
    urls = models.ManyToManyField(Url)

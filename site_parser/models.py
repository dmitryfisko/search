from django_hstore import hstore
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from django.db import models
from preferences.models import Preferences


class ParserPreferences(Preferences):
    __module__ = 'preferences.models'
    pool_size = models.IntegerField(default=20)
    default_requests_interval = models.FloatField(default=0.5)

    def __str__(self):
        return __name__


class Page(models.Model):
    url = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    lang = models.CharField(max_length=2, blank=True)
    search_index = VectorField()

    objects = models.Manager()
    search_manager = SearchManager(
        fields=('title', 'text'),
        config='pg_catalog.russian',
        search_field='search_index',
        auto_update_search_field=True
    )

    def __str__(self):
        return self.url


class WebSite(models.Model):
    domain = models.CharField(max_length=100, primary_key=True)
    pages = models.ManyToManyField(Page)

    graph_urls = hstore.DictionaryField()
    graph_connections = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    def __str__(self):
        return self.domain




from django_hstore import hstore
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from django.db import models

import dbsettings


class ParserSettings(dbsettings.Group):
    WORKER_POOL_SIZE = dbsettings.PositiveIntegerValue(default=20)
    REQUEST_MAX_TIMEOUT = dbsettings.PositiveIntegerValue(default=5)
    REQUEST_MIN_DELAY = dbsettings.FloatValue(default=0.5)

settings = ParserSettings('Parser Settings')


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
    graph_external = hstore.DictionaryField()
    objects = hstore.HStoreManager()

    def __str__(self):
        return self.domain

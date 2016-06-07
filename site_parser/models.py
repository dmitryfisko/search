from django_hstore import hstore
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from django.db import models


class Page(models.Model):
    url = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    search_index = VectorField()

    objects = models.Manager()
    search_manager = SearchManager(
        fields=('title', 'text'),
        config='pg_catalog.russian',
        search_field='search_index',
        auto_update_search_field=True
    )


class Site(models.Model):
    domain = models.CharField(max_length=100, primary_key=True)
    pages = models.ManyToManyField(Page)

    graph_urls = hstore.DictionaryField()
    graph_connections = hstore.DictionaryField()
    objects = hstore.HStoreManager()

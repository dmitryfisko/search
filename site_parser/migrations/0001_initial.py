# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-08 20:17
from __future__ import unicode_literals

from django.db import migrations, models
import django_hstore.fields
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('url', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('text', models.TextField(blank=True)),
                ('lang', models.CharField(blank=True, max_length=2)),
                ('search_index', djorm_pgfulltext.fields.VectorField(db_index=True, default='', editable=False, null=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('domain', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('graph_urls', django_hstore.fields.DictionaryField()),
                ('graph_connections', django_hstore.fields.DictionaryField()),
                ('pages', models.ManyToManyField(to='site_parser.Page')),
            ],
        ),
    ]

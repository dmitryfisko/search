# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 14:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='KeyValuePair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=240)),
                ('value', models.FloatField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('value', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('dictionary_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='site_parser.Dictionary')),
                ('domain', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('parse_iteration', models.IntegerField(default=0)),
            ],
            bases=('site_parser.dictionary',),
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('dictionary_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='site_parser.Dictionary')),
                ('path', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('parse_iteration', models.IntegerField(default=0)),
                ('urls_to', models.ManyToManyField(related_name='_url_urls_to_+', to='site_parser.Url')),
            ],
            bases=('site_parser.dictionary',),
        ),
        migrations.AddField(
            model_name='keyvaluepair',
            name='container',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_parser.Dictionary'),
        ),
        migrations.AddField(
            model_name='word',
            name='urls',
            field=models.ManyToManyField(to='site_parser.Url'),
        ),
        migrations.AddField(
            model_name='site',
            name='urls',
            field=models.ManyToManyField(to='site_parser.Url'),
        ),
    ]

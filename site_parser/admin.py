from django.contrib import admin

# Register your models here.

from site_parser.models import Page, WebSite

admin.site.register(Page)
admin.site.register(WebSite)

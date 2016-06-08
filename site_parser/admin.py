from django.contrib import admin

# Register your models here.
from preferences.admin import PreferencesAdmin

from site_parser.models import Page, WebSite, ParserPreferences

admin.site.register(Page)
admin.site.register(WebSite)

admin.site.register(ParserPreferences, PreferencesAdmin)
from django.contrib import admin

from preferences.admin import PreferencesAdmin
from search_api.models import APIPreferences


admin.site.register(APIPreferences, PreferencesAdmin)

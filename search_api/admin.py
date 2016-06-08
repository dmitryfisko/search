from django.contrib import admin

from preferences.admin import PreferencesAdmin
from search_api.models import ApiPreferences


admin.site.register(ApiPreferences, PreferencesAdmin)

from django.db import models
from preferences.models import Preferences


class ApiPreferences(Preferences):
    __module__ = 'preferences.models'
    search_page_limit = models.IntegerField(default=10)
    urls_upload_size_limit = models.IntegerField(default=1024*20)

    def __str__(self):
        return __name__

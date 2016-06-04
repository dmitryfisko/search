# -*- coding: utf8 -*-

from django.conf.urls import url

from .views import AddUrlReceiveView

urlpatterns = [
    url(r'(?P<bot_token>.+)/$', AddUrlReceiveView.as_view(), name='url'),
]

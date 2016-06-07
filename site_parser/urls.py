# -*- coding: utf8 -*-

from django.conf.urls import url

from .views import AddUrlReceiveView

urlpatterns = [
    url(r'^add$', AddUrlReceiveView.as_view(), name='url'),
]

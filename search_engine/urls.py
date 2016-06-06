from django.conf.urls import url, include
from django.contrib import admin
from search_engine import views

urlpatterns = [
    url(r'^$', views.search)
]

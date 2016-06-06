from django.conf.urls import url, include
from django.contrib import admin
from search_app import views

urlpatterns = [
    url(r'^$', views.index)
]

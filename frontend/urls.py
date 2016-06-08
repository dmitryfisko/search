from django.conf.urls import url, include
from django.contrib import admin
from frontend import views

urlpatterns = [
    url(r'^sitemap$', views.sitemap),
    url(r'^sitemap/draw', views.draw_sitemap),
    url(r'^$', views.index)
]

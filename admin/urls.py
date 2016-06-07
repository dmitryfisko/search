from django.conf.urls import url, include
from admin import views

urlpatterns = [
    url(r'^$', views.index)
]

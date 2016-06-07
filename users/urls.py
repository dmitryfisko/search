from django.conf.urls import url, include
from django.contrib import admin
from users import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^login/', login)
    # url(r'^login$', 'django.contrib.auth.views.login'),
    # url(r'^login', login)
]

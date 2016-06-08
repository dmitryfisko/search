"""search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from search_api.views import SearchReceiveView, AddUrlsReceiveView

urlpatterns = [
    url(r'^default_admin/', admin.site.urls),
    url(r'^admin/', include('urls_manage.urls')),
    # url(r'^urls/', include('site_parser.urls', namespace='site_parser')),
    # url(r'^search', include('search_engine.urls')),
    # url(r'^admin/', admin.site.urls),
    url(r'^api/urls', AddUrlsReceiveView.as_view(), name='api_add_urls'),
    url(r'^api/search/', SearchReceiveView.as_view(), name='api_search'),
    url(r'^', include('frontend.urls')),
]

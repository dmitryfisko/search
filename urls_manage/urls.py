from django.conf.urls import url, include
from urls_manage import views

urlpatterns = [
    url(r'^$', views.UrlList.as_view(), name='url_list'),
    url(r'^new$', views.UrlCreate.as_view(), name='url_new'),
    url(r'^delete/(?P<pk>\d+)$', views.UrlDelete.as_view(), name='url_delete'),
    url(r'^edit/(?P<pk>\d+)$', views.UrlUpdate.as_view(), name='url_edit')
]

from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.db import models
from urls_config.models import Url

class UrlList(ListView):
    model = Url

class UrlCreate(CreateView):
    model = Url
    success_url = reverse_lazy('url_list')
    fields = ['path', 'title']

class UrlUpdate(UpdateView):
    model = Url
    success_url = reverse_lazy('url_edit')
    fields = ['path', 'title']

class UrlDelete(DeleteView):
    model = Url
    success_url = reverse_lazy('url_delete')

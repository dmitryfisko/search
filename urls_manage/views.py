from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.db import models
from urls_manage.models import Url
from django.shortcuts import render

class UrlList(ListView):
    # import pdb; pdb.set_trace()
    model = Url

class UrlCreate(TemplateView):
    def get(self, request):
        return render(request, 'urls_manage/url_new.html')

    def post(self, request):
        # Send request to site parser
        path = request.POST.get('path')
        is_already_in_index = False

        text = ''
        if not is_already_in_index:
            text = 'URL will indexed soon'
        else:
            text = 'This URL was already indexed, but thanks for try'

        context = {
            'text': text
        }

        return render(request, 'urls_manage/added_to_index.html', context)

class UrlUpdate(UpdateView):
    # import pdb; pdb.set_trace()
    model = Url
    success_url = reverse_lazy('url_list')
    fields = ['path', 'title']

class UrlDelete(DeleteView):
    model = Url
    success_url = reverse_lazy('url_list')

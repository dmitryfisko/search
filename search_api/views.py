from django.http import JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from site_parser.models import Page


class SearchReceiveView(View):
    PAGE_LIMIT = 10

    @staticmethod
    def get(request):
        query = request.GET.get('q', None)
        start = request.GET.get('start', 0)

        if query:
            return SearchReceiveView.generate_response(query, start, request)
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def generate_response(query, start, request):
        limit = SearchReceiveView.PAGE_LIMIT
        results = Page.search_manager.search(query)[start:start+limit]
        response = render_to_response('search_api.html',
                                      {'results': results},
                                      context_instance=RequestContext(request))
        return response

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SearchReceiveView, self).dispatch(request, *args, **kwargs)

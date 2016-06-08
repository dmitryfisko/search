from django.http import JsonResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from search_api.utils import Snippet
from site_parser.models import Page
from site_parser.utils import convert_to_int


class SearchReceiveView(View):
    PAGE_LIMIT = 10

    @staticmethod
    def get(request):
        query = request.GET.get('q', None)
        start = request.GET.get('start', 0)
        start = convert_to_int(start)
        if start is None:
            start = 0

        if query:
            return SearchReceiveView.generate_response(query, start, request)
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def generate_response(query, start, request):
        limit = SearchReceiveView.PAGE_LIMIT
        all_results = Page.search_manager.search(query)
        results = all_results[start:start+limit]

        snippet = Snippet(query)
        response = {'response': {'results': [],
                                 'limit': limit,
                                 'count': len(all_results)}}
        for res in results:
            item = {'title': res.title,
                    'url': res.url,
                    'snippet': snippet.make_snippet(res.text)}
            response['response']['results'].append(item)

        # response = render_to_response('search_api.html',
        #                               {'results': results},
        #                               context_instance=RequestContext(request))
        return JsonResponse(response)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SearchReceiveView, self).dispatch(request, *args, **kwargs)

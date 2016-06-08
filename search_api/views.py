from django.http import JsonResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from search_api.utils import Snippet
from site_parser.models import Page
from site_parser.utils import convert_to_int

from site_parser.tasks import start_parser


class SearchReceiveView(View):
    PAGE_LIMIT = 10

    @staticmethod
    def get(request):
        # import pdb; pdb.set_trace()
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


class AddUrlsReceiveView(View):
    @staticmethod
    def get(request):
        start_url = request.GET.get('url', None)
        depth = request.GET.get('depth', None)

        if start_url:
            start_parser.delay(start_url, depth)
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({}, status=400)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddUrlsReceiveView, self).dispatch(request, *args, **kwargs)

import json

from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from search_api.utils import Snippet, ApiUtils
from site_parser.models import Page, Site
from site_parser.utils import convert_to_int

from site_parser.tasks import start_parser
import json


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
            return SearchReceiveView.generate_response(query, start)
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def generate_response(query, start):
        query, params = ApiUtils.extract_query_params(query)

        all_results = Page.search_manager.search(query)

        query_domain = params.get('site')
        if query_domain:
            site_filter = Site.objects.filter(domain=query_domain)
            if site_filter.exists():
                site_pages = Site.objects.get(domain=query_domain).pages.all()
                all_results &= site_pages
            else:
                all_results = Page.objects.none()

        query_lang = params.get('lang')
        if query_lang:
            all_results = all_results.filter(lang=query_lang)

        limit = SearchReceiveView.PAGE_LIMIT
        results = all_results[start:start + limit]

        snippet = Snippet(query)
        response = {'response': {'results': [],
                                 'limit': limit,
                                 'count': all_results.count()}}
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
    UPLOAD_MAX_SIZE = 1024 * 20

    def post(self, request):
        import pdb; pdb.set_trace()
        urls, depth = None, None
        urls_file = request.FILES.get('urls_file')
        if urls_file:
            json_data = urls_file.read()
        else:
            json_data = request.body

        urls_data = json.loads(json_data.decode('utf8'))

        if urls_data and len(json_data) <= self.UPLOAD_MAX_SIZE:
            depth, urls = ApiUtils.parse_urls_data(urls_data)

        if not urls:
            return HttpResponse(status=400)

        for url in urls:
            start_parser.delay(url, depth)

        return HttpResponse(status=200)


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddUrlsReceiveView, self).dispatch(request, *args, **kwargs)

import json

from django.http import JsonResponse
from django.http import HttpResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from search_api.utils import Snippet, ApiUtils
from site_parser.loader.utils import Utils
from site_parser.models import Page, Site
from site_parser.utils import convert_to_int, fix_schema

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
            return SearchReceiveView.generate_response(query, start)
        else:
            return JsonResponse({}, status=400)

    @staticmethod
    def generate_response(query, start):
        query, params = ApiUtils.extract_query_params(query)

        all_results = Page.search_manager.search(query)

        query_domain = params.get('site')
        if query_domain:
            urls = all_results.values_list('url', flat=True)
            # site_pages = Site.objects.get(domain=query_domain).pages
            # all_results = site_pages.filter(url_in=urls)
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
    UPLOAD_FILE_MAX_SIZE = 1024 * 20

    @staticmethod
    def get(request):
        start_url = request.GET.get('url', None)
        depth = request.GET.get('depth', None)

        if start_url:
            start_parser.delay(start_url, depth)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    def post(self, request):
        urls_file = request.FILES['urls_file']
        if urls_file.size <= self.UPLOAD_FILE_MAX_SIZE:
            depth, urls = self.parse_file(urls_file)
            if not urls:
                return HttpResponse('Wrong file format')

            for url in urls:
                start_parser.delay(url, depth)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)

    @staticmethod
    def parse_file(file):
        content = json.load(file)
        depth = content.get['depth']
        urls = content.get['urls']
        if urls and all(isinstance(url, str) for url in urls):
            urls = None
        return depth, urls

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddUrlsReceiveView, self).dispatch(request, *args, **kwargs)

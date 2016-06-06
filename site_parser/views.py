from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from site_parser.tasks import start_parser


class AddUrlReceiveView(View):
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
        return super(AddUrlReceiveView, self).dispatch(request, *args, **kwargs)
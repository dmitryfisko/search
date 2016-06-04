from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from site_parser.tasks import test


class AddUrlReceiveView(View):
    @staticmethod
    def post(request, bot_token):
        test.delay(bot_token)
        return JsonResponse({}, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AddUrlReceiveView, self).dispatch(request, *args, **kwargs)
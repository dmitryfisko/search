from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import os
from search.settings import BASE_DIR

# Create your views here.
@api_view(['POST'])
def search(request):
    print(request.data)
    # import pdb; pdb.set_trace()
    with open(os.path.join(BASE_DIR, "search_engine\\static\\search_engine\\test.json")) as file:
        search_results = json.load(file)
    return Response(search_results)

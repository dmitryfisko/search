from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def search(request):
    print(request.data)
    # import pdb; pdb.set_trace()
    search_results = [
        {
            'header': 'Kittens',
            'preview': 'fjdjakdjkajkjadks'
        },
        {
            'header': 'Kittens',
            'preview': 'fjdjakdjkajkjadks'
        },
        {
            'header': 'Kittens',
            'preview': 'fjdjakdjkajkjadks'
        },
        {
            'header': 'Kittens',
            'preview': 'fjdjakdjkajkjadks'
        },
        {
            'header': 'Kittens',
            'preview': 'fjdjakdjkajkjadks'
        },
    ]
    return Response(search_results)
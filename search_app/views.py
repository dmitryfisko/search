from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'search_app/index.html')
    
def results(request):
    return render(request, 'search_app/results.html')
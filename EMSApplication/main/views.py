from django.http import HttpResponse
from django.shortcuts import  render

# Create your views here.

def index (response):
    return HttpResponse("<h1>Test page</h1>")
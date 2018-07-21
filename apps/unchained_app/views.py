from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def index(request):
    response="Hello World"
    return HttpResponse(response)
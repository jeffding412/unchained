from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, "unchained_app/index.html")
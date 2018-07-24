from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Shipping, Product, Image, Offer

# Create your views here.
def index(request):
    return render(request, "unchained_app/index.html")

def login_or_register(request):
    user = User.objects.filter(email=request.POST['email'])
    request.session['errors'] = User.objects.validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    if len(user) == 0:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(email=request.POST['email'],password_hash=pw_hash,first_name="",last_name="",rating=0,num_sold=0,isAdmin=False)
    
    return redirect('/')
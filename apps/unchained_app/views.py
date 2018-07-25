from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Shipping, Product, Image, Offer

# Create your views here.
def index(request):
    return render(request, "unchained_app/index.html")

def adminLoginForm(request):
    return render(request, "/unchained/admin.html")

def adminProducts(request):
    return render(request, "/unchained/admin_products.html")

def adminProductById(request):
    return render(request, "/unchained/admin_product_id.html")

def adminEdit(request, productId):
    context = {
        "productId": productId
    }
    return render(request, "/unchained/admin_editProduct.html", context)

def adminDelete(request, productId):
    return redirect("/admin/products")

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
        user = User.objects.create(email=request.POST['email'],password_hash=pw_hash,username="",first_name="",last_name="",rating=0,num_sold=0,isAdmin=False)
        request.session['user_id'] = user.id
    else:
        request.session['user_id'] = user[0].id

    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def add_product(request):
    if not "user_id" in request.session:
        return redirect('/logout')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": user
    }
    return render(request, "unchained_app/add_product.html", context)
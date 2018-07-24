from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt

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
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Shipping, Product, Image, Offer

# Create your views here.
def index(request):
    return render(request, "unchained_app/index.html")

<<<<<<< HEAD
=======
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

>>>>>>> origin/master
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

<<<<<<< HEAD
def adminLoginForm(request):
    if "curUserId" in request.session["curUserId"]:
        if User.objects.get(id=request.session["curUserId"]).isAdmin:
            return redirect("/admin/products")
        return redirect("/products")

    return render(request, "/unchained/admin.html")

def adminLogin(request):
    if request.method != "POST":
        return redirect("/")

    errors = User.objects.validator_admin(request.POST)

    if len(errors) > 0:
        return redirect("/admin")

    request.session["curUserId"] = User.objects.get(email=request.POST["email"]).id
    return redirect("/admin/products")

def adminProducts(request):
    if "curUserId" not in request.session["curUserId"]:
        return redirect("/")

    context = {
        "products": Product.objects.all()
    }
    
    return render(request, "/unchained/admin_products.html", context)

def adminProductById(request, productId):
    if "curUserId" not in request.session["curUserId"]:
        return redirect("/")
    
    product = Product.objects.get(id=productId)
    seller = Seller.objects.get(id=product.seller_id)
    context = {
        "product": product,
        "seller": seller,
        "shipping": seller.shippings.first()
    }

    return render(request, "/unchained/admin_product_id.html")

def adminEdit(request, productId):
    if "curUserId" not in request.session["curUserId"]:
        return redirect("/")

    context = {
        "product": Product.objects.get(id=productId)
    }
    return render(request, "/unchained/admin_editProduct.html", context)

def adminProcessEdit(request, productId):
    if request.method != "POST":
        if User.objects.get(id=request.session["curUserId"]).isAdmin:
            return redirect("/admin/products")
        return redirect("/products")

    errors = Product.objects.validator(request.POST)

    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tages=tag)
        return redirect("/admin/products/" + str(productId) + "/edit")

    product = Product.objects.get(id=productId)
    product.name = request.POST["name"]
    product.brand = request.POST["brand"]
    product.description = request.POST["description"]
    product.category = request.POST["category"]
    product.image = request.POST["image"]
    product.save()

    return redirect("/admin/products/" + str(productId))

def adminDelete(request, productId):
    if "curUserId" not in request.session["curUserId"]:
        return redirect("/")

    # make sure none admins can't access product deleting route
    if not User.objects.get(id=request.session["curUserId"]).isAdmin:
        return redirect("/logout")

    delProduct = Product.objects.get(id=productId)
    delProduct.delete()

    return redirect("/admin/products")

def logout(request):
    request.session.clear()
    redirect("/")

=======
def logout(request):
    request.session.clear()
    return redirect('/')
>>>>>>> origin/master

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
        user = User.objects.create(email=request.POST['email'],password_hash=pw_hash,username="",first_name="",last_name="",rating=0,num_sold=0,isAdmin=False)
        request.session['user_id'] = user.id
    else:
        request.session['user_id'] = user[0].id

    return redirect('/')

def adminLoginForm(request):
    if "curUserId" in request.session.keys():
        if "curUserId" not in request.session.keys():
            return redirect("/")

        if User.objects.get(id=request.session["curUserId"]).isAdmin:
            return redirect("/admins/products")
        return redirect("/products")

    return render(request, "unchained_app/admin.html")

def adminLogin(request):
    if request.method != "POST":
        return redirect("/")

    errors = User.objects.validator_admin(request.POST)

    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, tag)
        return redirect("/admins")

    request.session["curUserId"] = User.objects.get(email=request.POST["email"]).id
    return redirect("/admins/products")

def adminProducts(request):
    if "curUserId" not in request.session.keys():
        return redirect("/")

    if len(Product.objects.filter(id=productId)) == 0:
        return redirect("/admins/products")

    context = {
        "products": Product.objects.all()
    }

    return render(request, "unchained_app/admin_product_id.html", context)

def add_product(request):
    if not "user_id" in request.session:
        return redirect('/logout')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": user
    }

    return render(request, "unchained_app/add_product.html")

def adminProductById(request, productId):
    if "curUserId" not in request.session.keys():
        return redirect("/")

    if len(Product.objects.filter(id=productId)) == 0:
        return redirect("/admins/products")

    product = Product.objects.get(id=productId)
    seller = User.objects.get(id=product.seller_id)

    context = {
        "product": product,
        "seller": seller,
        "shipping": seller.shippings.first()
    }

    return render(request, "unchained_app/admin_product_id.html", context)

def adminEdit(request, productId):
    if "curUserId" not in request.session.keys():
        return redirect("/")

    if not User.objects.get(id=request.session["curUserId"]).isAdmin:
        return redirect("/logout")

    if len(Product.objects.filter(id=productId)) == 0:
        return redirect("/admins/products")

    context = {
        "product": Product.objects.get(id=productId)
    }

    return render(request, "unchained_app/admin_editProduct.html", context)

def adminProcessEdit(request, productId):
    if request.method != "POST":
        if User.objects.get(id=request.session["curUserId"]).isAdmin:
            return redirect("/admins/products")
        return redirect("/products")

    errors = Product.objects.validator(request.POST)

    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tages=tag)
        return redirect("/admins/products/" + str(productId) + "/edit")

    product = Product.objects.get(id=productId)
    product.name = request.POST["name"]
    product.brand = request.POST["brand"]
    product.description = request.POST["description"]
    product.category = request.POST["category"]
    product.image = request.POST["image"]
    product.save()

    return redirect("/admin/products/" + str(productId))

def adminDelete(request, productId):
    if "curUserId" not in request.session.keys():
        return redirect("/")

    # make sure none admins can't access product deleting route
    if not User.objects.get(id=request.session["curUserId"]).isAdmin:
        return redirect("/logout")

    delProduct = Product.objects.get(id=productId)
    delProduct.delete()

    return redirect("/admin/products")

def logout(request):
    request.session.clear()
    return redirect("/")

def add_product_to_id(request, id):
    if not "user_id" in request.session:
        return redirect('/logout')

    request.session['errors'] = Product.objects.validator(request.POST)
    if len(request.session['errors']):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in request.session['errors'].items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/addProduct')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        "user": user
    }    

    Product.objects.create(name=request.POST['name'],brand=request.POST['brand'],category=request.POST['category'],price=float(request.POST['price']),description=request.POST['description'],status="For Sale",seller_id=user)

    print(Product.objects.all().values())

    return redirect('/')
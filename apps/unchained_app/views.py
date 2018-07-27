from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from .models import User, Shipping, Product, Image, Offer

# Create your views here.
def index(request):
    context = {
    'products' : Product.objects.all()
    }
    return render(request, "unchained_app/index.html", context)

def login_or_register(request):
    user = User.objects.filter(email=request.POST['email'])
    request.session['errors'] = User.objects.validator(request.POST)
    if len(request.session['errors']):
        # redirect the user back to the form to fix the errors
        return redirect('/')

    if len(user) == 0:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(email=request.POST['email'],password_hash=pw_hash,username="",first_name="",last_name="",rating=0,num_sold=0,isAdmin=False)
        Shipping.objects.create(first_name="",last_name="",address="",city="",state="",country="",zipcode="",user_id=user)
        request.session['user_id'] = user.id
    else:
        request.session['user_id'] = user[0].id

    return redirect('/')

def adminLoginForm(request):
    if "curUserId" in request.session.keys():
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
            messages.error(request, error, extra_tags=tag)
        return redirect("/admins")

    request.session["curUserId"] = User.objects.get(email=request.POST["email"]).id
    return redirect("/admins/products")

def adminProducts(request):
    if "curUserId" not in request.session.keys():
        return redirect("/")

    if not User.objects.get(id=request.session["curUserId"]).isAdmin:
        return redirect("/logout")

    context = {
        "products": Product.objects.all()
    }

    return render(request, "unchained_app/admin_products.html", context)

@csrf_exempt
def adminAllProducts(request):
    if request.method != "POST":
        return redirect("/")

    products = Product.objects.all()

    context = {
        "products": Product.objects.all()
    }

    return render(request, "unchained_app/admin_products_table.html", context)

def adminSearch(request):
    if request.method != "POST":
        return redirect("/")

    tempProds = Product.objects.filter(name__icontains=request.POST["productName"]).filter(category__contains=request.POST["categories"])
    products = []

    for product in tempProds:
        seller_name = (product.seller_id.first_name + " " + product.seller_id.last_name).lower()
        if request.POST["sellerName"].lower() in seller_name:
            products.append(product)

    context = {
        "products": products
    }

    return render(request, "unchained_app/admin_products_table.html", context)

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
    seller = User.objects.get(id=product.seller_id.id)

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

    errors = Product.objects.validator_admin(request.POST)

    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect("/admins/products/" + str(productId) + "/edit")

    product = Product.objects.get(id=productId)
    product.name = request.POST["name"]
    product.brand = request.POST["brand"]
    product.description = request.POST["description"]
    product.category = request.POST["category"]
    product.image = request.POST["image"]
    product.save()

    return redirect("/admins/products/" + str(productId))

def adminDelete(request, productId):
    if "curUserId" not in request.session.keys():
        return redirect("/")

    # make sure none admins can't access product deleting route
    if not User.objects.get(id=request.session["curUserId"]).isAdmin:
        return redirect("/logout")

    delProduct = Product.objects.get(id=productId)
    delProduct.delete()

    return redirect("/admins/products")

def logout(request):
    request.session.clear()
    return redirect("/")

def add_product_to_id(request, id):
    if not "user_id" in request.session:
        return redirect('/logout')

    request.session['errors'] = Product.objects.validator(request.POST)
    if len(request.session['errors']):
        # redirect the user back to the form to fix the errors
        return redirect('/addProduct')

    user = User.objects.get(id=request.session['user_id'])

    Product.objects.create(name=request.POST['name'],brand=request.POST['brand'],category=request.POST['category'],price=int(request.POST['price']),description=request.POST['description'],status="For Sale",seller_id=user)

    return redirect('/')

def settings(request, id):
    if not "user_id" in request.session:
        return redirect('/logout')

    user = User.objects.get(id=request.session['user_id'])
    shipping_info = Shipping.objects.get(user_id=user.id)
    context = {
        "user": user,
        "shipping": shipping_info
    }    

    return render(request, "unchained_app/settings.html", context)

def update_profile(request):
    if not "user_id" in request.session:
        return redirect('/logout')

    user = User.objects.get(id=request.session['user_id'])

    request.session['errors'] = User.objects.update_validator(request.POST)
    if len(request.session['errors']):
        # redirect the user back to the form to fix the errors
        return redirect('/settings/' + str(user.id))

    user.first_name = request.POST['first']
    user.last_name = request.POST['last']
    user.email = request.POST['email']
    user.username = request.POST['username']
    user.save()

    return redirect('/settings/' + str(user.id))

def change_password(request):
    if not "user_id" in request.session:
        return redirect('/logout')

    user = User.objects.get(id=request.session['user_id'])

    request.session['errors'] = User.objects.change_password_validator(request.POST)
    if len(request.session['errors']):
        # redirect the user back to the form to fix the errors
        return redirect('/settings/' + str(user.id))

    pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user.password_hash = pw_hash
    user.save()

    return redirect('/settings/' + str(user.id))

def change_shipping(request):
    if not "user_id" in request.session:
        return redirect('/logout')

    user = User.objects.get(id=request.session['user_id'])
    
    request.session['errors'] = Shipping.objects.validator(request.POST)
    if len(request.session['errors']):
        # redirect the user back to the form to fix the errors
        return redirect('/settings/' + str(user.id))

    shipping = Shipping.objects.get(user_id=user.id)
    shipping.first_name = request.POST['first_name']
    shipping.last_name = request.POST['last_name']
    shipping.address = request.POST['address']
    shipping.city = request.POST['city']
    shipping.state = request.POST['state']
    shipping.country = request.POST['country']
    shipping.zipcode = request.POST['zip']
    shipping.save()

    return redirect('/settings/' + str(user.id))

def myProducts(request):
    if not "user_id" in request.session:
        return redirect('/logout')

    user = User.objects.get(id=request.session['user_id'])
    products = Product.objects.filter(seller_id=user)

    context = {
        'user': user,
        'products': products
    }

    return render(request, "unchained_app/myProducts.html", context)

def editProduct(request, id):
    if not "user_id" in request.session:
        return redirect('/logout')

    request.session['errors'] = Product.objects.validator(request.POST)
    if len(request.session['errors']):
        # redirect the user back to the form to fix the errors
        return redirect('/myProducts')

    product = Product.objects.get(id=id)
    product.name = request.POST['name']
    product.brand = request.POST['brand']
    product.category = request.POST['category']
    product.price = int(request.POST['price'])
    product.description = request.POST['description']
    product.save()

    return redirect('/myProducts')

def soldProduct(request, id):
    if not "user_id" in request.session:
        return redirect('/logout')

    product = Product.objects.get(id=id)
    product.status = "Sold"
    product.save()

    return redirect('/myProducts')

def product_page(request, id):
    if not "user_id" in request.session:
        return redirect('/logout')

    product = Product.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    if user.num_sold != 0:
        average = user.rating/user.num_sold
    else:
        average = -1

    context = {
        "product": product,
        "user": user,
        "rating": average
    }

    return render(request, 'unchained_app/product_page.html', context)

def user_messages(request, id):
    if not "user_id" in request.session:
        return redirect('/logout')

    

    return render(request, "unchained_app/user_messages.html")  

def make_offer(request, id):
    if not "user_id" in request.session:
        return redirect('/logout')

    request.session['errors'] = Offer.objects.validator(request.POST)
    if len(request.session['errors']):
        # redirect the user back to the form to fix the errors
        return redirect('/product/'+id)

    product = Product.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])

    Offer.objects.create(price=request.POST['price'],message=request.POST['message'],product_id=product,user_id=user)

    return redirect('/messages/'+str(request.session['user_id']))
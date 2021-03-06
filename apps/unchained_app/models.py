from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
PRICE_REGEX = re.compile(r"^\d+$")

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors["email"] = "User email is a required field"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "User email is not in valid format"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        user = User.objects.filter(email=postData['email'])
        if user and not bcrypt.checkpw(postData['password'].encode(), user[0].password_hash.encode()):
            errors['failure'] = "No email/password combo"

        return errors

    def validator_admin(self, postData):
        errors = {}

        user = User.objects.filter(email=postData["email"])
        if len(user) == 1 and bcrypt.checkpw(postData['password'].encode(), user[0].password_hash.encode()):
            if not user[0].isAdmin:
                errors["adminLogin"] = "You do not have permission to login admin area"

        elif len(user) == 0 or not bcrypt.checkpw(postData['password'].encode(), user[0].password_hash.encode()):
            errors["adminLogin"] = "Incorrect Email or Password"
            
        return errors

    def update_validator(self, postData):
        errors = {}

        if len(postData['email']) < 1:
            errors["email"] = "User email is a required field"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "User email is not in valid format"

        if len(postData['first']) < 2:
            errors["first"] = "User first name should be at least 2 characters"
        elif not re.match(r"^[a-zA-Z]+$", postData['first']):
            errors["first"] = "User first name can only contain letters"

        if len(postData['last']) < 2:
            errors["last"] = "User last name should be at least 2 characters"
        elif not re.match(r"^[a-zA-Z]+$", postData['first']):
            errors["last"] = "User last name can only contain letters"

        if len(postData['username'].replace(" ", "")) < 1:
            errors["username"] = "Username can't be blank"
            
        return errors

    def change_password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors["failure"] = "Password should be at least 8 characters"
        elif postData['password'] != postData['confirm']:
            errors["failure"] = "Passwords do not match"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    rating = models.FloatField()
    num_sold = models.IntegerField()
    isAdmin = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class ShippingManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name must have 2+ characters"
        elif not postData["first_name"].isalpha():
            errors["first_name"] = "Letters only for first name"

        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name must have 2+ characters"
        elif not postData["last_name"].isalpha():
            errors["last_name"] = "Letters only for last name"
        
        if len(postData["address"].replace(" ", "")) < 8:
            errors["address"] = "Address must be at least 8 characters long"

        city = postData["city"].replace(" ", "")

        if len(city) < 2:
            errors["city"] = "City name must have 2+ letters"
        elif not city.isalpha():
            errors["city"] = "Letters only for city name"

        if len(postData["state"]) != 2:
            errors["state"] = "State must be an abbreviation of 2 capital letters"
        elif not postData["state"].isalpha():
            errors["state"] = "Letters only for state"

        if len(postData["country"]) < 2:
            errors["country"] = "Country must have 2+ letters"
        elif not postData["country"].isalpha():
            errors["country"] = "Letters only for country"

        testZip = postData["zip"]
        if len(str(testZip)) != 5:
            errors["zip"] = "Zip code must have exactly 5 numbers"
        elif not testZip.isnumeric():
            errors["zip"] = "Numbers only for zip code"

        return errors

class Shipping(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    
    user_id = models.ForeignKey(User, related_name="shippings")

    objects = ShippingManager()


class ProductManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData["name"]) < 1:
            errors["name"] = "Name cannot be blank"

        if len(postData["brand"]) < 1:
            errors["brand"] = "Brand cannot be blank"

        if len(postData["category"]) < 1:
            errors["cateogry"] = "category cannot be blank"
        elif not postData["category"].isalpha():
            errors["category"] = "Letters only for category"

        if not PRICE_REGEX.match(str(postData["price"])):
            errors["price"] = "Invalid price"

        if len(postData["description"].replace(" ", "")) < 1:
            errors["description"] = "Description cannot be blank"

        return errors

    def validator_admin(self, postData):
        errors = {}

        if len(postData["name"]) < 1:
            errors["name"] = "Name cannot be blank"

        if len(postData["brand"]) < 1:
            errors["brand"] = "Brand cannot be blank"

        if len(postData["category"]) < 1:
            errors["category"] = "category cannot be blank"
        elif not postData["category"].isalpha():
            errors["category"] = "Letters only for category"

        if len(postData["description"].replace(" ", "")) < 1:
            errors["description"] = "Description cannot be blank"

        return errors

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length=255)

    seller_id = models.ForeignKey(User, related_name="products")

    objects = ProductManager()

class ImageManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if (not postData["file"].name.endswith(".jpg")) and (not postData["file"].name.endswith(".jpeg")) and (not postData["file"].name.endswith(".png")):
            errors["file"] = "File must be in jpg, jpeg, or png format"

        return errors

class Image(models.Model):
    name = models.CharField(max_length=255)
    imageFile = models.FileField(upload_to="apps/unchained_app/static/unchained_app/images2")
    product_id = models.ForeignKey(Product, related_name="images")

    objects = ImageManager()


class OfferManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if not PRICE_REGEX.match(str(postData["price"])):
            errors["price"] = "Invalid price"

        if len(postData["message"].replace(" ", "")) < 1:
            errors["message"] = "Message cannot be blank"

        return errors

class Offer(models.Model):
    price = models.IntegerField()
    product_id = models.ForeignKey(Product, related_name="offers")
    user_id = models.ForeignKey(User, related_name="offers")
    seller = models.ForeignKey(User, related_name="sell_offers")
    message = models.TextField()

    objects = OfferManager()

class ReplyManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['reply'].replace(" ", "")) < 1:
            errors['reply'] = "Reply cannot be blank"

        return errors

class Reply(models.Model):
    message = models.TextField()
    offer = models.ForeignKey(Offer, related_name="replies")
    user_id = models.ForeignKey(User, related_name="replier")
    
    objects = ReplyManager()


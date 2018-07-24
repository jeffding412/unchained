from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

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
        if not user:
            errors['failure'] = "No email/password combo"
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password_hash.encode()):
            errors['failure'] = "No email/password combo"

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
        return errors

class Shipping(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=255)
    zip = models.IntegerField()
    
    user_id = models.ForeignKey(User, related_name="shippings")

    objects = ShippingManager()


class ProductManager(models.Manager):
    def validator(self, postData):
        errors = {}
        return errors

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    status = models.CharField(max_length=255)

    seller_id = models.ForeignKey(User, related_name="products")

    objects = ProductManager()


class ImageManager(models.Manager):
    def validator(self, postData):
        errors = {}
        return errors

class Image(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, related_name="images")

    objects = ImageManager()


class OfferManager(models.Manager):
    def validator(self, postData):
        errors = {}
        return errors

class Offer(models.Model):
    price = models.FloatField()
    product_id = models.ForeignKey(Product, related_name="offers")
    user_id = models.ForeignKey(User, related_name="offers")
    message = models.TextField()

    objects = OfferManager()


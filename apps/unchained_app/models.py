from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
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


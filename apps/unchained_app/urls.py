from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^admins$', views.adminLoginForm, name="adminLoginForm"),
    url(r'^admins/login$', views.adminLogin, name="adminLogin"),
    url(r'^admins/products$', views.adminProducts, name="adminProducts"),
    url(r'^admins/products/(?P<productId>\d+)$', views.adminProductById, name="adminProductId"),
    url(r'^admins/products/(?P<productId>\d+)/edit$', views.adminEdit, name="adminEdit"),
    url(r'^admins/products/(?P<productId>\d+)/processEdit$', views.adminProcessEdit, name="adminProcessEdit"),
    url(r'^admins/products/(?P<productId>\d+)/delete$', views.adminDelete, name="adminDelete"),
    url(r'^loginOrRegister$', views.login_or_register),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^addProduct$', views.add_product),
]
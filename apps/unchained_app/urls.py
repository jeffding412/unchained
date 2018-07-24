from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^loginOrRegister$', views.login_or_register),
    url(r'^admin$', views.adminLoginForm, name="adminLoginForm"),
    url(r'^admin/login$', views.adminLogin, name="adminLogin"),
    url(r'^admin/products$', views.adminProducts, name="adminProducts"),
    url(r'^admin/products/(?P<productId>\d+)$', views.adminProductById, name="adminProductId"),
    url(r'^admin/products/(?P<productId>\d+)/edit$', views.adminEdit, name="adminEdit"),
    url(r'^admin/products/(?P<productId>\d+)/delete$', views.adminDelete, name="adminDelete"),
    url(r'^admin/products/(?P<productId>\d+)/processEdit$', views.adminProcessEdit, name="adminProcessEdit"),
    url(r'^logout$', views.logout, name="logout")
]
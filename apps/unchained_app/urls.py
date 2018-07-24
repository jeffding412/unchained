from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin$', views.adminLoginForm, name="adminLogin"),
    url(r'^admin/products$', views.adminProducts, name="adminProducts"),
    url(r'^admin/products/(?P<productId>\d+)$', views.adminProductById, name="adminProductId"),
    url(r'^admin/products/(?P<productId>\d+)/edit$', views.adminEdit, name="adminEdit"),
    url(r'^admin/products/(?P<productId>\d+)/delete$', views.adminDelete, name="adminDelete")
]
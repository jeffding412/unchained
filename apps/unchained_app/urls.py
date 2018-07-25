from django.conf.urls import url
from . import views

urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.index, name="index"),
    url(r'^admins$', views.adminLoginForm, name="adminLoginForm"),
    url(r'^admins/login$', views.adminLogin, name="adminLogin"),
    url(r'^admins/products$', views.adminProducts, name="adminProducts"),
    url(r'^admins/products/(?P<productId>\d+)$', views.adminProductById, name="adminProductId"),
    url(r'^admins/products/(?P<productId>\d+)/edit$', views.adminEdit, name="adminEdit"),
    url(r'^admins/products/(?P<productId>\d+)/processEdit$', views.adminProcessEdit, name="adminProcessEdit"),
    url(r'^admins/products/(?P<productId>\d+)/delete$', views.adminDelete, name="adminDelete"),
=======
    url(r'^$', views.index),
    url(r'^admin$', views.adminLoginForm, name="adminLogin"),
    url(r'^admin/products$', views.adminProducts, name="adminProducts"),
    # url(r'^admin/products/(?P<productId>\d+)$', views.adminProductById, name="adminProductId") I think this was deleted
    url(r'^admin/products/(?P<productId>\d+)/edit$', views.adminEdit, name="adminEdit"),
    url(r'^admin/products/(?P<productId>\d+)/delete$', views.adminDelete, name="adminDelete"),
>>>>>>> 5290daf3a930aadc2fa912cc58e8ec79b0ab087d
    url(r'^loginOrRegister$', views.login_or_register),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^addProduct$', views.add_product),
    url(r'^addProduct/(?P<id>\d+)', views.add_product_to_id)
]
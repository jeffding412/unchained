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
    url(r'^admins/allProducts$', views.adminAllProducts, name="adminAllProducts"),
    url(r'^admins/search$', views.adminSearch, name="adminSearch"),
    url(r'^loginOrRegister$', views.login_or_register),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^addProduct$', views.add_product),
    url(r'^addProduct/(?P<id>\d+)$', views.add_product_to_id),
    url(r'^messages/(?P<id>\d+)$', views.myMessages),
    url(r'^settings/(?P<id>\d+)$', views.settings),
    url(r'^updateProfile$', views.update_profile),
    url(r'^changePassword$', views.change_password),
    url(r'^changeShipping$', views.change_shipping),
    url(r'^myProducts$', views.myProducts),
    url(r'^edit/product/(?P<id>\d+)$', views.editProduct),
    url(r'^sold/(?P<id>\d+)$', views.soldProduct),
    url(r'^product/(?P<id>\d+)$', views.product_page)
]
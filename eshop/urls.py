from django.urls import path, re_path
from . import views

app_name = 'eshop'

urlpatterns = [
    path('', views.index, name="index"),
    path('cart/', views.cart, name='cart'),
    path('order/checkout/', views.checkout, name='checkout'),
    path('category/', views.category, name='category'),
    path('category/<slug:slug>/', views.category, name='category'),
    #re_path(r'^category/(?P<slug>[\w-]+)/*$', views.category, name='category'),
    path('product/<slug:slug>/', views.product, name='product'),

    path('contact/', views.contact, name='contact'),
]

from django.urls import path, re_path
from . import views

app_name = 'eshop'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('order/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('category/', views.ProductListView.as_view(), name='category'),
    path('category/<slug:slug>/', views.ProductListView.as_view(), name='category'),
    #re_path(r'^category/(?P<slug>[\w-]+)/*$', views.category, name='category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product'),

    path('contact/', views.ContactView.as_view(), name='contact'),

]

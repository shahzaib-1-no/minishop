from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add-product-to-cart/<int:product_id>', views.add_product_to_cart, name='add_product_to_cart'),
    path('remove-product-from-cart/<int:product_id>', views.remove_product_from_cart, name='remove_product_from_cart'),
]
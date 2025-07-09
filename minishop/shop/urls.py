from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/detail/', views.product_detail, name='product_detail'),
    

]
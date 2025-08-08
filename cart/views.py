from django.shortcuts import render
from dashboard.models import Product
from django.contrib import messages
from django.shortcuts import redirect
from .models import CartItem
from django.db import transaction
from cart.services.cart_services import (add_product_to_cart_service, 
                                         get_user_cart,
                                         delete_product_from_cart_service,
                                         )
# Create your views here.


def cart(request):
    cart_items, cart_total = get_user_cart(request)
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total
    }
    return render(request, 'cart/cart.html', context)
        

def add_product_to_cart(request, product_id):
    success, message = add_product_to_cart_service(request, product_id)
    if success:
        messages.success(request, message)
        return redirect('cart')
    else:
        messages.error(request, message)
        return redirect('shop')
    
def remove_product_from_cart(request, product_id):
    success, message = delete_product_from_cart_service(request, product_id)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('cart')
 
        
    

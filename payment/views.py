from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (Address,)
from .forms import AddressForm
from payment.services.payment_services import (CheckoutServices)

# Create your views here.
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:  # Check if cart is empty or None
        messages.error(request, 'Cart is empty')
        return redirect('cart')
        
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            terms_accepted = form.cleaned_data.get('terms_accepted')
            if terms_accepted:
                checkout_services = CheckoutServices()
                success, message = checkout_services.handle_payment_method(request,form)
                if success:
                    # If Stripe, redirect to Stripe checkout page (session URL)
                    if form.cleaned_data.get('method') == 'STRIPE':
                        return redirect(message)  # message contains Stripe session URL

                    messages.success(request, message)
                    return redirect('checkout')
                else:
                    messages.error(request, message)
                    return redirect('checkout')
                
    else:
        form = AddressForm()
    context={
        'form':form,
        'button': 'Submit',
    }
    return render(request, 'payment/checkout.html', context)

def shop_cancel(request):
    return render(request, 'payment/cancel.html')

def success(request):
    checkout_services = CheckoutServices()
    success, message = checkout_services.stripe_payment_success(request)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
        
    return render(request, 'payment/success.html')


from django.db import transaction
from payment.models import (Address, Payment, Order, OrderItem, Refund, ReturnRequest)
from dashboard.models import Product
from django.contrib.auth.models import User
from payment.forms import AddressForm
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth import login
import uuid
import os
import json
from dotenv import load_dotenv ## pip install python-dotenv
import stripe
load_dotenv()

class CheckoutServices:
        
    def handle_payment_method(self, request, form):
        """
        Handles payment method selection. 
        Adds address to database
        Returns: bool, str
        """
        try:
            ## Check if form is valid
            if form.is_valid():
                account = False
                ## Check if terms and conditions are accepted
                if not form.cleaned_data.get('terms_accepted'):
                    return False, 'Please accept the terms and conditions.'
                ## Check if account creation is enabled
                account_create = form.cleaned_data.get('account_create')
                if account_create:
                    account= True
                    return False, 'Account creation not implemented yet.'
                ## Save address to database
                address =form.save(commit=False)
                address.save()
                ## Get address ID
                address_id = address.id
                ## Get payment method
                payment_method = form.cleaned_data.get('method')
                ## Match payment method
                match payment_method:
                    case 'COD':
                        return False, 'Cash on Delivery not implemented yet'
                    case 'STRIPE':
                        return self._stripe(request, address_id,account)
                    case 'PAYPAL':
                        return False, 'PayPal not implemented yet'
                    case 'CREDIT_CARD':
                        return False, 'Credit Card not implemented yet'
                    case _:
                            return False, 'Invalid Payment Method'
        except Exception as e:
            return False, f"An error occurred: {str(e)}"

    def _stripe(self, request, address_id, account):
        """
        Stripe payment handling logic
        Create Checkout Session from cart
        Includes: Tax and Service Charges
        Returns: bool, str
        Payment Checkout: Success URL and Cancel URL
        """
        SECRET_KEY = os.getenv('STRIPE_SECRET_KEY') ## Stripe Secret Key
        
        try:
            ## Check if Stripe Secret Key is set
            if SECRET_KEY:
                ## Set Stripe API Key
                stripe.api_key = SECRET_KEY
                ## Check if cart exists
                cart= request.session.get('cart')
                if not cart:
                    return False, 'Cart Is Empty'
                ## Create line items
                line_items = []
                ## Iterate over cart items
                for item,key in cart.items():
                    try: ## Check if product exists
                        product = Product.objects.get(id=key['id'])
                    except Product.DoesNotExist:
                        return False, f"Product Does Not Exist. Product ID: {key['id']}"
                    
                    line_items.append({ ## Adding item to line_items
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(key['price']*100),## Stripe use cents ,Convert price to cents
                            'product_data': {
                                'name': product.name,
                            },
                        },
                        'quantity': key['quantity'],
                    })
                ## Adding Tax to line_items Optional
                line_items.append({ 
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(50*100),## Stripe use cents ,Convert price to cents
                        'product_data': {
                            'name': "Tax",
                        },
                    },
                    'quantity': 1,
                })
                ## Adding Service Charges to line_items Optional
                line_items.append({ 
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(100*100),## Stripe use cents ,Convert price to cents
                        'product_data': {
                            'name': "Service Charges",
                        },
                    },
                    'quantity': 1,
                })
                ## Get Domain from env
                domain = os.getenv('DOMAIN')
                ## Check if domain is set
                if not domain:
                    if settings.DEBUG:## If DEBUG is True, use localhost
                        domain = 'http://localhost:8000'
                    else: ## If DEBUG is False, Show the error message
                        return False, 'Domain is not set'
                ## Append domain to success and cancel URLs
                success_url = f"{domain}/payment/success/?session_id={{CHECKOUT_SESSION_ID}}"
                cancel_url = f"{domain}/payment/cancel/?session_id={{CHECKOUT_SESSION_ID}}"
                ## Create Stripe Checkout Session
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=success_url,
                    cancel_url=cancel_url,
                    metadata={
                        'address_id': str(address_id),
                        'account': str(account),
                    },
                )
                return True, session.url
                
            else:
                return False, 'Invalid Secret Key'
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False, f"An error occurred: {str(e)}"
    
    def stripe_payment_success(self, request):
        ## Get Session ID from request
        session_id = request.GET.get('session_id')
        if session_id:## If Session ID is not None
            try:
                SECRET_KEY = os.getenv('STRIPE_SECRET_KEY') ## Stripe Secret Key
                stripe.api_key = SECRET_KEY ## Add Stripe Secret Key to Stripe API
                ## Retrieve Stripe Checkout Session from Session ID
                session = stripe.checkout.Session.retrieve(session_id)
                ## Check if session is paid
                if session.payment_status == 'paid':
                    address_id = int(session.metadata['address_id'])
                    ## Add data to database
                    return self._adding_data_to_database(request, address_id, session)
                    
                else:
                    return False, f"Payment Not Completed: {session.payment_status}"
            except stripe.error.StripeError as e:
                print(f"StripeError: {str(e)}")
                return False, f"StripeError: {str(e)}"
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return False, f"An error occurred: {str(e)}"
        else:
            return False, "Session_id not found"
    
    def _adding_data_to_database(self, request, address_id, session):
        """
        Updates payment_draft to APPROVED
        Creates Payment, Order and OrderItem
        Returns: bool, str
        """
        try:
            with transaction.atomic():
                """
                Create User if account creation is enabled
                transaction.atomic() is used to make sure that the 
                database is updated only once. If an error occurs,
                the database will not be updated.
                """
                ## Get Amount from session, divide by 100 to get amount.
                amount = session.amount_total/100
                account = session.metadata['account']
                if not request.user.is_authenticated:
                    if account:
                        try:
                            ## Create User
                            email = f"user_{address_id}@example.com"
                            user = User.objects.filter(email=email).first()
                            if not user:
                                username = f"user_{address_id}_{uuid.uuid4().hex[:6]}"
                                raw_password = get_random_string(10)  # Agar zaroor ho show/send kar do
                                user = User.objects.create_user(
                                    username=username,
                                    email=email,
                                    password=raw_password,
                                )
                            login(request, user)
                        except Exception as e:
                            return False, f"An error occurred: {str(e)}"
                ## Get Address from database
                address=Address.objects.filter(id=address_id).first()
                ## Check if payment draft is not approved
                if not address.payment_draft=='APPROVED':
                    ## Update payment_draft to APPROVED
                    address.payment_draft='APPROVED'
                    ## Save Address to database
                    address.save()
                ## Create Payment
                payment,created_payment = Payment.objects.get_or_create(
                    transaction_id=session.payment_intent,
                    amount=amount,
                    paid_at= timezone.now(),
                    is_paid=True,
                )
                payment.save()
                ## Get User
                user= request.user if request.user.is_authenticated else None
                ## Create Order
                order,created_order = Order.objects.get_or_create(
                    user = user,
                    payment=payment,
                    address=address,
                    total_price=amount,
                    status='PROCESSING',
                )
                order.save()
                ## Check if order is created
                if created_order:
                    ## Get Cart from session
                    cart= request.session.get('cart')
                    ## Iterate over cart items
                    for item,key in cart.items():
                        try: ## Check if product exists
                            product= Product.objects.get(id=key['id'])
                        except Product.DoesNotExist:
                            return False, f"Product Does Not Exist. Product ID: {key['id']}"
                        ## Create OrderItem
                        order_item= OrderItem.objects.create(
                            order=order,
                            product=product,
                            quantity=key['quantity'],
                            price=product.price,
                        )
                        order_item.save()
                    request.session.pop('cart', None) # Remove cart from session
                    request.session.modified = True # Mark session as changed for saving
                    
            return True, f"Payment Successful. Order ID: {order.order_number}"
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False, f"An error occurred: {str(e)}"


            
            
            
            
                
        

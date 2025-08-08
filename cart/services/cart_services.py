from django.db import transaction
from cart.models import CartItem
from dashboard.models import Product
from django.contrib.auth.models import User


def add_product_to_cart_service(request, product_id):
    if request.user.is_authenticated:
        try:
            with transaction.atomic():
                product= Product.objects.get(id=product_id)
                cart_item,created = CartItem.objects.get_or_create(
                    user=request.user, 
                    product=product,
                    defaults={
                        'product_name': product.name,
                        'product_price': product.price,
                        'quantity': 1,
                    }
                )
                if not created:
                    if cart_item.quantity <= product.quantity:
                        cart_item.quantity += 1
                        cart_item.save()
                        return True, 'Product Added To Cart'
                    else:
                        return False, 'Product Quantity Exceeded'
        except Product.DoesNotExist:
            return False, 'Product Does Not Exist'
        return True, 'Product Added To Cart'
    else:
        # Get existing cart from session or initialize empty dict if not found
        cart= request.session.get('cart',{})
        product_id_str = str(product_id) # Ensure key is a string for consistent session storage
        if product_id_str in cart:
            get_product = cart.get(product_id_str)
            # Sometimes users may tamper with session (via browser tools), 
            # so you should ensure cart item is well-formed before using .
            # get() on it.
            if not isinstance(get_product,dict):
                return False, 'Cart Data Is Corrupted'
            # Safely update quantity and total price
            quantity = int(get_product.get('quantity'))+1
            price = float(get_product.get('price'))
            total= float(price*quantity)
            cart[product_id_str]['quantity'] = quantity
            cart[product_id_str]['total'] = total
            # Save updated cart back to session
            request.session['cart'] = cart
            request.session.modified = True # Mark session as changed for saving
            return True, 'Quantity is Increased,Product Is Already In Cart'
        else:
            # Product not in cart — fetch from DB
            try:
                product= Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return False, 'Product Does Not Exist'
            # Add product to cart with initial quantity of 1
            quantity=1
            price= float(product.price)
            cart[product_id_str] = {
                'id': product.pk,
                'name': product.name,
                'price': price,
                'quantity': quantity,
                'total': float(price*quantity),
                'image': product.image.url
            }
            request.session['cart'] = cart
    request.session.modified = True  # Ensure Django saves session even if object not reassigned
    return True, 'Product Added To Cart'


def get_user_cart(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        items = []
        total = 0
        for item in cart_items:
            item_total = item.product_price * item.quantity
            total += item_total
            items.append({
                'id': item.product.id,
                'name': item.product_name,
                'price': item.product_price,
                'quantity': item.quantity,
                'total': item_total,
                'image': item.product.image.url
            })
    else:
        cart = request.session.get('cart', {})
        items = list(cart.values())
        total = sum(float(item['total']) for item in items)
        
    return items, total


def delete_product_from_cart_service(request, product_id):
    if request.user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
            cart_item.delete()
            return True, 'Product Removed From Cart'
        except CartItem.DoesNotExist:
            return False, 'Product Does Not Exist'
    else:
        cart= request.session.get('cart',{})
        product_id_str = str(product_id) # Ensure key is a string for consistent session storage
        if product_id_str in cart:
            get_product = cart.get(product_id_str)
            # Sometimes users may tamper with session (via browser tools), 
            # so you should ensure cart item is well-formed before using .
            # get() on it.
            if not isinstance(get_product,dict):
                return False, 'Cart Data Is Corrupted'
            del cart[product_id_str]
            request.session['cart'] = cart
            request.session.modified = True # Mark session as changed for saving
            return True, 'Product Removed From Cart'
        else:
            return False, 'Product Does Not Exist'

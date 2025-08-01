from django.conf import settings

def landing_page(request):
    cart = request.session.get('cart', {})
    count = len(cart)
    return {
        'cart_count': count
    }
from django.conf import settings
from cart.models import CartItem
def landing_page(request):
    if request.user.is_authenticated:
        count= CartItem.objects.filter(user=request.user).count()
    else:    
        cart = request.session.get('cart', {})
        count = len(cart)
    return {
        'cart_count': count
    }
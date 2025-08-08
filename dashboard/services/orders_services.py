from django.conf import settings
from django.db.models import Count
from payment.models import (Address, Payment, Order,
                            Product, OrderItem, Refund, ReturnRequest)



class OrdersServices:
    def orders_list(self, request):
        try:
            orders= Order.objects.prefetch_related('items').order_by('-id')
            return True, 'Orders List Fetched', orders
        except Exception as e:
            return False, f"An error occurred: {e}", None
    
    def orders_details(self, request, pk):
        try:
            order = Order.objects.prefetch_related('items__returns__refund').get(order_uuid=pk)
            return True, 'Order Details Fetched', order
        except Exception as e:
            return False, f"An error occurred: {e}", None
        
    
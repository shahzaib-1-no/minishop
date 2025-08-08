from django.db.models.signals import post_save
from django.dispatch import receiver
from payment.models import Order, ReturnRequest
from dashboard.models import Notification
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user or None,
            message=f"Order Placed: {instance.order_number}. Order ID: {instance.order_number}",
            notification_type='order_placed',
            is_read=False,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )
        
@receiver(post_save, sender=ReturnRequest)
def create_return_request(sender, instance, created, **kwargs):
    if created:
        order = instance.order_item.order
        user_name= order.user.first_name if order.user else 'Anonymous'
        Notification.objects.create(
            user=instance.order_item.order.user or None,
            message=f"Return request submitted from User : {user_name} (Order #{order.order_number})",
            notification_type='order_returned',
            is_read=False,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
        )
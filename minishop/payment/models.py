from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import uuid
from django.db import transaction
from dashboard.models import Product
from django.utils import timezone
from django.urls import reverse
# Create your models here.

# ------------------ Address Model ------------------
class Address(models.Model):
    PAYMENT_CHOICES = [
        ('COD','Cash on delivery'),
        ('STRIPE','Stripe'),
        ('PAYPAL','Paypal'),
        ('CREDIT_CARD','Credit Card'),
    ]
    PAYMENT_DRAFT= [
        ('DRAFT','Draft'),
        ('APPROVED','Approved'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    payment_draft= models.CharField(max_length=255, choices=PAYMENT_DRAFT, default='DRAFT')
    account_create= models.BooleanField(default=False, help_text="Create new account")
    terms_accepted = models.BooleanField(default=False, help_text="I have read and accept the terms and conditions")
    method= models.CharField(max_length=255, choices=PAYMENT_CHOICES, default='STRIPE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# ------------------ Payment Model ------------------
class Payment(models.Model):
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_at = models.DateTimeField(blank=True, null=True)

# ------------------ Order Model ------------------
class Order(models.Model):
    ORDER_STATUS=[
        ('PENDING','Pending'),
        ('PROCESSING','Processing'),
        ('SHIPPED','Shipped'),
        ('COMPLETED','Completed'),
        ('CANCELLED','Cancelled'),
        ('RETURNED','Returned'),
    ]
    order_uuid= models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_number= models.CharField(unique=True, null=True, blank=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True , related_name='orders')
    address= models.ForeignKey(Address, on_delete=models.PROTECT, related_name='orders')
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT, related_name='order')
    status= models.CharField(max_length=255, choices=ORDER_STATUS, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            with transaction.atomic():
                last_order = Order.objects.select_for_update().order_by('-id').first()
                if last_order and last_order.order_number:
                    last_number = int(last_order.order_number.replace('ORD-', ''))
                    self.order_number = f"ORD-{last_number + 1:06d}"
                else:
                    self.order_number = "ORD-000001"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.order_number} - {self.status}"
    
    def get_absolute_url(self):
        return reverse('order_details', kwargs={'pk': self.order_uuid})

# ------------------ OrderItem Model ------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('dashboard.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of price
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} = {self.total}"

# ------------------ ReturnRequest Model ------------------
class ReturnRequest(models.Model):
    RETURN_STATUS=[
        ('DRAFT','Draft'),
        ('REQUESTED','Requested'),
        ('APPROVED','Approved'),
        ('REJECTED','Rejected'),
        ('RECIEVED','Recieved'),
    ]
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='returns')
    reason = models.CharField(max_length=255)
    status= models.CharField(max_length=255, choices=RETURN_STATUS, default='DRAFT')
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_refund_initiated = models.BooleanField(default=False)

    def __str__(self):
        return f"Return for {self.order_item} - {self.status}"

# ------------------ Refund Model ------------------
class Refund(models.Model):
    return_request = models.OneToOneField(ReturnRequest, on_delete=models.CASCADE, related_name='refund')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway_ref = models.CharField(max_length=100, blank=True, null=True, help_text="Refund ID from Stripe/PayPal")
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='refunds_processed')
    is_completed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.is_completed and not self.processed_at:
            self.processed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Refund for {self.return_request.order_item.product.name} - {'Completed' if self.is_completed else 'Pending'}"
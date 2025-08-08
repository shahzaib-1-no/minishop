from django.db import models
from dashboard.models import Product
from django.contrib.auth.models import User

# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def get_total(self):
        """Return total price for this cart item."""
        return self.product_price * self.quantity

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"


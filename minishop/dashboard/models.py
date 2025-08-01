from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# Create your models here.
class navbar(models.Model):
    name = models.CharField(max_length=100)
    number= models.IntegerField()
    email= models.CharField(max_length=100)
    description= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class banner(models.Model):
    image = models.ImageField(upload_to='banner/')
    name = models.CharField(max_length=100)
    title= models.CharField(max_length=100)
    description= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class services(models.Model):
    icon = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description= models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class landingPage(models.Model):
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title    

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcategories',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('name', 'parent')  # DB-level constraint

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check for duplicate category name under the same parent
        existing = Category.objects.filter(
            name__iexact=self.name,
            parent=self.parent
        ).exclude(id=self.id)

        if existing.exists():
            if self.parent:
                raise ValidationError(
                    f"A sub-category named '{self.name}' already exists under '{self.parent.name}'."
                )
            else:
                raise ValidationError(
                    f"A main category named '{self.name}' already exists."
                )

        # Auto-generate slug if not provided
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product/')
    quantity = models.IntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='sub_categories',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Notification(models.Model):
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['created_at']),
        ]
    NOTIFICATION_CHOICES = [
        # User-related
        ('user_registered', 'New User Registered'),
        ('user_profile_updated', 'User Profile Updated'),

        # Order-related
        ('order_placed', 'Order Placed'),
        ('order_shipped', 'Order Shipped'),
        ('order_delivered', 'Order Delivered'),
        ('order_cancelled', 'Order Cancelled'),
        ('order_returned', 'Order Returned'),

        # Messaging
        ('support_reply', 'Support Team Replied'),
        ('user_message', 'New User Message'),

        # System
        ('system_alert', 'System Alert'),
        ('maintenance_notice', 'Scheduled Maintenance'),

        # Marketing/Custom
        ('promo_offer', 'New Promotional Offer'),
        ('custom', 'Custom Notification'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=55, choices=NOTIFICATION_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
     # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.notification_type} → {self.message[:50]}"


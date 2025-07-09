from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
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
    
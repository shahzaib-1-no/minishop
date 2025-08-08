"""
pip install Faker factory_boy requests
    Faker → Fake data generate karega (name, description, price).
    Factory Boy → Django model ke liye factory create karega.
    Requests → Placeholder image download karne ke liye.
"""

import factory
from faker import Faker
from django.core.files.base import ContentFile
from dashboard.models import Product, Category
from payment.models import (Address, Payment, Order, OrderItem, Refund, ReturnRequest)
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction
import os
import random


fake = Faker()

def get_random_static_image():
    static_images_path = os.path.join(settings.BASE_DIR,"media","product")
    images = [img for img in os.listdir(static_images_path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        random_image_path = os.path.join(static_images_path, random.choice(images))
        with open(random_image_path, "rb") as f:
            return ContentFile(f.read(), name=os.path.basename(random_image_path))
    return None

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        
    category = factory.LazyFunction(
    lambda: random.choice(list(Category.objects.filter(parent__isnull=False))) 
    if Category.objects.filter(parent__isnull=False).exists() else None
    )
    name = factory.LazyAttribute(
        lambda self: f"{self.category.name} {fake.word().title()} {fake.bothify(text='??-###')}"
        if self.category else fake.word().title()
    )
    price = factory.LazyAttribute(
        lambda _: round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2)
    )
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=20))
    quantity = factory.LazyAttribute(lambda _: fake.pyint(min_value=1, max_value=10))
    image= factory.LazyFunction(get_random_static_image)
 
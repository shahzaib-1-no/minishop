
from django.core.management.base import BaseCommand
from dashboard.factories import ProductFactory
from dashboard.models import Category

class Command(BaseCommand):
    help = "Seed 200 products with category-specific online images."

    def handle(self, *args, **kwargs):
        sub_categories = Category.objects.filter(parent__isnull=False)
        if not sub_categories.exists():
            self.stdout.write(self.style.ERROR("No sub-categories found."))
            return
        
        batch_size = 200
        ProductFactory.create_batch(batch_size)

        self.stdout.write(self.style.SUCCESS(f"{batch_size} products created successfully!"))

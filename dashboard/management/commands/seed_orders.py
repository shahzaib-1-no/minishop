from django.core.management.base import BaseCommand
from dashboard.order_factories import OrderFactory

class Command(BaseCommand):
    help = "Seed 6 orders."
    def handle(self, *args, **kwargs):
        batch_size = 6
        OrderFactory.create_batch(batch_size)

        self.stdout.write(self.style.SUCCESS(f"{batch_size} orders created successfully!"))
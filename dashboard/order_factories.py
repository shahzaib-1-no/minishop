import factory

from faker import Faker
from dashboard.models import Product
from payment.models import Address, Payment, Order, OrderItem, Refund, ReturnRequest
from django.contrib.auth.models import User
from django.utils import timezone
import random
fake = Faker()

# ---------------- User Factory ----------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.LazyFunction(fake.user_name) 
    email = factory.LazyFunction(fake.email)
    password = factory.PostGenerationMethodCall('set_password', '12345')
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)

# ---------------- Address Factory ----------------
class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    user = factory.SubFactory(UserFactory)
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    phone = factory.LazyFunction(lambda: fake.random_number(digits=9))
    email = factory.LazyFunction(fake.email)
    country = factory.LazyFunction(fake.country)
    city = factory.LazyFunction(fake.city)
    postal_code = factory.LazyFunction(fake.postcode)
    apartment = factory.LazyFunction(fake.building_number)
    address = factory.LazyFunction(fake.street_address)
    payment_draft = factory.Iterator(['DRAFT', 'APPROVED'])
    account_create = factory.LazyFunction(lambda: random.choice([True, False]))
    terms_accepted = True
    method = factory.Iterator(['COD', 'STRIPE', 'PAYPAL', 'CREDIT_CARD'])
    created_at = factory.LazyFunction(timezone.now)

# ---------------- Payment Factory ----------------
class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    transaction_id = factory.LazyFunction(fake.uuid4)
    is_paid = True
    amount = factory.LazyAttribute(lambda o: random.choice(Product.objects.all()).price)
    paid_at = factory.LazyFunction(timezone.now)

# ---------------- Order Factory ----------------
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    address = factory.SubFactory(AddressFactory)
    payment = factory.SubFactory(PaymentFactory)
    status = factory.Iterator(['PENDING', 'PROCESSING', 'SHIPPED', 'COMPLETED', 'RETURNED'])
    total_price = factory.LazyAttribute(lambda o: random.choice(Product.objects.all()).price)
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)

    @factory.post_generation
    def create_items(self, create, extracted, **kwargs):
        if not create:
            return
        total= 0
        num_products = random.randint(1,10)
        for _ in range(num_products):
            product = random.choice(Product.objects.all())
            quantity = random.randint(1,6)
            order_item = OrderItem.objects.create(
                order=self,
                product=product,
                quantity=quantity,
                price=product.price,
                total=product.price * quantity,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            total += order_item.total
            
            if self.status == 'RETURNED':
                return_status = random.choice(['DRAFT', 'REQUESTED', 'APPROVED', 'REJECTED', 'RECIEVED'])
                return_request = ReturnRequest.objects.create(
                    order_item=order_item,
                    reason=fake.text(max_nb_chars=100),
                    status=return_status,
                    requested_at=timezone.now(),
                    updated_at=timezone.now(),
                    is_refund_initiated=True if return_status == 'APPROVED' else False,
                )
                if return_status == 'APPROVED':
                    Refund.objects.create(
                        return_request=return_request,
                        amount=product.price,
                        gateway_ref=fake.uuid4(),
                        processed_by=self.user,
                        is_completed=True,
                        processed_at=timezone.now(),
                        created_at=timezone.now(),
                        notes=fake.text(max_nb_chars=20),
                    )
        self.total_price = total
        self.save()

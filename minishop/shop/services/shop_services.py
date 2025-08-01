from django.core.paginator import Paginator
from dashboard.models import Product

class ShopServices:
    def get_category_products(self, request, slug):
        try:
            product = Product.objects.filter(category__slug=slug).prefetch_related('category').order_by('-id')
            paginator = Paginator(product, 10)
            page_number = request.GET.get('page')
            products = paginator.get_page(page_number)
            return True, 'Products Listed', products
        except Exception as e:
            return False, f"An error occurred: {e}", None
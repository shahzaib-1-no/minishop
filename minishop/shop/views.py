from django.shortcuts import render
from dashboard.models import ( Category, Product)
from django.db.models import Count
from django.core.paginator import Paginator
from shop.services.shop_services import ShopServices
# Create your views here.

def shop(request):
    product= Product.objects.all().prefetch_related('category').order_by('-id')
    paginator = Paginator(product, 10)
       
    # Current page number get karega
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    category = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories').order_by('-id')
    category_data = []

    for cat in category:
        cat_data = {
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'parent': cat.parent.id if cat.parent else None,
            'sub_count': cat.subcategories.count(),
            'sub_categories': []
        }

        for sub_cat in cat.subcategories.all().order_by('-id'):
            cat_data['sub_categories'].append({
                'id': sub_cat.id,
                'name': sub_cat.name,
                'slug': sub_cat.slug,
                'parent': sub_cat.parent.id if sub_cat.parent else None
            })

        category_data.append(cat_data)
    context={
        'category_data':category_data,
        'products':products,
    }
    return render(request, 'shop/shop.html', context)

def product_detail(request, slug):
    product= Product.objects.get(slug=slug)
    context={
        'product':product,
    }
    return render(request, 'shop/product_detail.html', context)

def category_products(request, slug):
    shop_service = ShopServices()
    success, message, products = shop_service.get_category_products(request, slug)
    if not success:
        return render(request, 'shop/shop.html', message)
    category = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories').order_by('-id')
    category_data = []

    for cat in category:
        cat_data = {
            'id': cat.id,
            'name': cat.name,
            'slug': cat.slug,
            'parent': cat.parent.id if cat.parent else None,
            'sub_count': cat.subcategories.count(),
            'sub_categories': []
        }

        for sub_cat in cat.subcategories.all().order_by('-id'):
            cat_data['sub_categories'].append({
                'id': sub_cat.id,
                'name': sub_cat.name,
                'slug': sub_cat.slug,
                'parent': sub_cat.parent.id if sub_cat.parent else None
            })

        category_data.append(cat_data)
    context={
        'products':products,
        'category_data':category_data,
    }
    return render(request, 'shop/shop.html', context)
    
    

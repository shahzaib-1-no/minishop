from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import  login as auth_login, logout as auth_logout
from .models import (navbar, banner, services, Category, Product )
from payment.models import Order
from .forms import (navbarForm, bannerForm, servicesForm, CategoryForm, productForm)
from django.db.models import Count
from dashboard.services.orders_services import OrdersServices
from .services.dashboard_services import DashboardServices, DashboardChartsServices
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from dashboard.models import Notification
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import JsonResponse

# Create your views here.

def is_admin(user):
    return user.is_superuser

def is_vendor(user):
    return not user.is_superuser

def vendor_dashboard(request):
    is_superuser = request.user.is_superuser
    if is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')
    
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    dashboard_services= DashboardServices()
    data= dashboard_services.get_cards()   
    context={
        'data':data
    }
    return render(request, 'dashboard/admin_dashboard.html',context)

@login_required
@user_passes_test(is_vendor)
def user_dashboard(request):
    return render(request, 'dashboard/user_dashboard.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

### Navbar Section ###

@login_required
@user_passes_test(is_admin)
def navbar_create(request):
    data,created = navbar.objects.get_or_create(id=1)
    if request.method == "POST":
        form= navbarForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Nav-Bar Data Updated")
            return redirect('vendor_dashboard')
    else:
        form= navbarForm(instance=data)
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/navbar/create.html', context)

### Navbar Section End ###

### Notification Section ###
@login_required
@user_passes_test(is_admin)
def notification_redirect_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    return redirect(notification.related_object.get_absolute_url())
### Notification Section End ###

### Dashboard Section ###
@login_required
@user_passes_test(is_admin)
def order_chart_data(request):
    dashboard_charts= DashboardChartsServices()
    orders_charts= dashboard_charts.get_chats()
    context={
        'orders_charts':orders_charts
    }
    return JsonResponse(context['orders_charts'], safe=False)

@login_required
@user_passes_test(is_admin)
def weekly_chart_data(request):
    dashboard_charts= DashboardChartsServices()
    orders_charts= dashboard_charts.get_orders_weekly_chart_data()
    context={
        'orders_charts':orders_charts
    }
    return JsonResponse(context['orders_charts'], safe=False)
### Dashboard Section End ###


### Banner Section ###
@login_required
@user_passes_test(is_admin)
def banner_create(request):
    if request.method == "POST":
        form= bannerForm(request.POST, request.FILES )
        if form.is_valid():
            form.save()
            messages.success(request, "Banner Data Created")
            return redirect('vendor_dashboard')
    else:
        form= bannerForm()
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/banner/create.html', context)

@login_required
@user_passes_test(is_admin)
def banner_list(request):
    data = banner.objects.all()
    context={
        'data':data
    }
    return render(request, 'dashboard/admin_pages/banner/list.html', context)

@login_required
@user_passes_test(is_admin)
def banner_update(request, pk):
    data = get_object_or_404(banner, pk=pk)
    if request.method == "POST":
        form= bannerForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner Data Updated")
            return redirect('banner_list')
    else:
        form= bannerForm(instance=data)
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/banner/create.html', context)

@login_required
@user_passes_test(is_admin)
def banner_delete(request, pk):
    data = get_object_or_404(banner, pk=pk)
    data.delete()
    messages.success(request, "Banner Data Deleted")
    return redirect('banner_list')
### Banner Section End ###

### Services Section ###
@login_required
@user_passes_test(is_admin)
def services_create(request):
    if request.method == "POST":
        form= servicesForm(request.POST, request.FILES )
        if form.is_valid():
            form.save()
            messages.success(request, "Services Data Created")
            return redirect('vendor_dashboard')
    else:
        form= servicesForm()
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/services/create.html', context)


@login_required
@user_passes_test(is_admin)
def services_list(request):
    data = services.objects.all().order_by('-id')
    context={
        'data':data
    }
    return render(request, 'dashboard/admin_pages/services/list.html', context)

@login_required
@user_passes_test(is_admin)
def services_update(request, pk):
    data = get_object_or_404(services, pk=pk)
    if request.method == "POST":
        form= servicesForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Services Data Updated")
            return redirect('services_list')
    else:
        form= servicesForm(instance=data)
    context={
        'form':form
    }
    return render(request, 'dashboard/admin_pages/services/create.html', context)

@login_required
@user_passes_test(is_admin)
def services_delete(request, pk):
    data = get_object_or_404(services, pk=pk)
    data.delete()
    messages.success(request, "Services Data Deleted")    
    return redirect('services_list')
### Services Section End ###

### Category Section ###
@login_required
@user_passes_test(is_admin)
def category_create(request):
    # Get only main categories (those without a parent) and count sub-categories    
    main_categories = Category.objects.filter(parent__isnull=True) \
        .annotate(sub_count=Count('subcategories')) \
        .order_by('-id')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category Created')
            return redirect('category_create')
    else:
        form = CategoryForm()
    context = {
        'form': form,
        'button': 'Create',
        'data': main_categories
    }
    return render(request, 'dashboard/admin_pages/category/create.html', context)

@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):
    data = get_object_or_404(Category, pk=pk)
    data.delete()
    messages.success(request, 'Category Deleted')
    return redirect('category_create')

### Categroy  Section End ###

### Product Section ###
@login_required
@user_passes_test(is_admin)
def product_create(request):
    if request.method == "POST":
        form= productForm(request.POST, request.FILES )
        if form.is_valid():
            form.save()
            messages.success(request, "Product Data Created")
            return redirect('product_create')
    else:
        form= productForm()
    context={
        'form':form,
        'button': 'Create',
    }

    return render(request, 'dashboard/admin_pages/product/create.html', context)

class ProductList(BaseDatatableView):
    model = Product
    columns = ['Sno','image', 'title', 'price', 'quantity', 'category', 'created_at', 'updated_at', 'action']
    order_columns = ['id','image', 'name', 'price', 'quantity', 'category', 'created_at', 'updated_at', 'action']
    search_fields = ['name', 'price', 'quantity', 'category__name', 'created_at', 'updated_at']
    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', None)
        if search_value:
            q = Q()
            for field in self.search_fields:
                q |= Q(**{f"{field}__icontains": search_value})
            qs = qs.filter(q)
            return qs
        return qs
    def render_column(self, row, column):
        if column == 'action':
            return format_html(
                '''
                <a href="{}" class="btn btn-sm btn-primary"><i class="fas fa-pen"></i></a>
                <a href="{}" class="btn btn-sm btn-danger" onclick="return confirm('Are you sure?');">
                    <i class="fas fa-trash"></i>
                </a>
                ''',
                reverse('product_update', args=[row.id]),
                reverse('product_delete', args=[row.id])
            )
        elif column == 'image':
            return format_html(
                '<img src="{}" class="img-thumbnail" width="150" alt="Current Image">', 
                row.image.url
            )
        else:
            return super().render_column(row, column)
    def prepare_results(self, qs):
        """Convert queryset into list of dicts instead of list of lists"""
        data = []
        for index, item in enumerate(qs, start=1):
            data.append({
                'Sno': index,
                'image': self.render_column(item, 'image'),
                'name': item.name,
                'price': f"${item.price:.2f}",
                'quantity': item.quantity,
                'category': item.category.name if item.category else '',
                'created_at': item.created_at.strftime("%Y-%m-%d"),
                'updated_at': item.updated_at.strftime("%Y-%m-%d"),
                'action': self.render_column(item, 'action'),
            })
        return data

@login_required
@user_passes_test(is_admin)
def product_list_page(request):
    return render(request, 'dashboard/admin_pages/product/list.html')

@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    data = get_object_or_404(Product, pk=pk)
    data.delete()
    messages.success(request, 'Product Deleted')
    return redirect('product_list')

@login_required
@user_passes_test(is_admin)
def product_update(request, pk):
    data = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form= productForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Data Updated")
            return redirect('product_list')
    else:
        form= productForm(instance=data)
    context={
        'form':form,
        'button': 'Update',
    }
    return render(request, 'dashboard/admin_pages/product/create.html', context)

### Product Section End ###


### Orders Section ###
@login_required
@user_passes_test(is_admin)
def orders_list(request):
    return render(request, 'dashboard/admin_pages/orders/list.html')

class OrdersListData(BaseDatatableView):
    model = Order
    columns = ['Sno', 'order', 'customer', 'status', 'payment', 'total', 'date', 'action']
    order_columns = ['id','', 'order_number', 'address__first_name', 'status', 'address__method', 'total_price', 'created_at', ''] 
    search_fields = ['order_number', 'address__first_name', 'address__email', 'status', 'address__method', 'total_price', 'created_at']
    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', None)
        if search_value:
            q = Q()
            for field in self.search_fields:
                q |= Q(**{f"{field}__icontains": search_value})
            qs = qs.filter(q)
        return qs


    ## render_column
    def render_column(self, row, column):
        if column == 'action':
            return format_html(
                '''
                <a href="{}" class="btn btn-sm btn-view" title="View Order"><i class="fas fa-eye"></i></a>
                
                ''',
                reverse('order_details', args=[row.order_uuid])
            )
        elif column == 'status':
            return mark_safe(self.render_status(row.status))
        elif column == 'customer':
            return f'{row.address.first_name} <br><small>{row.address.email}</small>'
        elif column == 'payment':
            return row.address.method
        else:
            return super().render_column(row, column)
    def render_status(self, status):
        status = status.lower()
        if status in ['completed', 'complete']:
            return '<span class="status completed">Completed</span>'
        elif status == 'pending':
            return '<span class="status pending">Pending</span>'
        elif status in ['cancelled', 'canceled']:
            return '<span class="status cancelled">Cancelled</span>'
        elif status == 'processing':
            return '<span class="status processing">Processing</span>'
        elif status == 'shipped':
            return '<span class="status shipped">Shipped</span>'
        elif status == 'refunded':
            return '<span class="status refunded">Refunded</span>'
        return f'<span class="status">{status.title()}</span>'
    def prepare_results(self, qs):
        """Convert queryset into list of dicts instead of list of lists"""
        data = []
        for index,item in enumerate(qs, start=1):
            data.append({
                'Sno': index,
                'order': item.order_number,
                'customer': f'{item.address.first_name}<br><small>{item.address.email}</small>',
                'status': self.render_status(item.status),
                'payment': item.address.method,
                'total': f"${item.total_price:.2f}",
                'date': item.created_at.strftime("%Y-%m-%d"),
                'action': self.render_column(item, 'action'),
            })
        return data

@login_required
@user_passes_test(is_admin)
def order_details(request, pk):
    success, message, data = OrdersServices().orders_details(request, pk)
    items= data.items.all()
    count= count = items.values('product').distinct().count()
    if not success:
        messages.error(request, message)
    context={
        'data':data,
        'total_items':count
    }
    return render(request, 'dashboard/admin_pages/orders/details.html', context)
### Orders Section End ###
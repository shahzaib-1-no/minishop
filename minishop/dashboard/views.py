from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import  login as auth_login, logout as auth_logout
from .models import (navbar, banner, services, Category, Product)
from .forms import (navbarForm, bannerForm, servicesForm, CategoryForm, productForm)
from django.db.models import Count
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
    return render(request, 'dashboard/admin_dashboard.html')

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

@login_required
@user_passes_test(is_admin)
def product_list(request):
    data = Product.objects.all().order_by('-id')
    context={
        'data':data
    }
    return render(request, 'dashboard/admin_pages/product/list.html', context)

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
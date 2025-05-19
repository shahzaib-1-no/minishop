from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import  login as auth_login, logout as auth_logout
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

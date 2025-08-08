from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import (SignUpForm, loginForm)
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
# Create your views here.
def home(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/pages/about/about.html')

def contact(request):
    return render(request, 'home/pages/contact/contact.html')

def login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Welcome Back')
                return redirect('vendor_dashboard')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('login')
    else:
        form = loginForm()
    return render(request, 'home/pages/auth/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                auth_login(request, user)
                messages.success(request, 'Welcome Back')
                return redirect('vendor_dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'home/pages/auth/register.html', {'form': form})
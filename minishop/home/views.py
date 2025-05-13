from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/pages/about/about.html')

def contact(request):
    return render(request, 'home/pages/contact/contact.html')
from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.object.all()
    return render(request, 'products/home.html', {'products':products})
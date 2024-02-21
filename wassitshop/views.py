from django.shortcuts import render
from store.models import Product

def home(requests):
     
     products=Product.objects.all().filter(is_available=True)

     context={
          'products':products,
     }
     return render(requests,'home.html',context)
from django.shortcuts import render 
from django.http import HttpResponse 
from .models import products,dishes

def fproducts(request):
	 product = products.objects.all()
	 return render(request, "cook/products.html", {"product": product})

def fdishes(request):
	 dish = dishes.objects.all()
	 return render(request, "cook/products.html", {"product": dish})





def index(request):
	 return render(request, "cook/index.html")
def copy(request):
	 return render(request, "cook/copy.html")
# Create your views here.

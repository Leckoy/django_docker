from django.shortcuts import render 
from django.http import HttpResponse 
from .models import Ingredient,Dish

def fproducts(request):
	products = Ingredient.objects.all()
	return render(request, "cook/products.html", {"products": products})

def fdishes(request):
	dish = Dish.objects.all()
	return render(request, "cook/products.html", {"product": dish})





def index(request):
	return render(request, "cook/index.html")
def copy(request):
	return render(request, "cook/copy.html")
# Create your views here.

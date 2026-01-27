from django.shortcuts import render 
from django.http import HttpResponse 
from .models import products

def about(request):
	 product = products.objects.all()
	 return render(request, "test/about.html", {"product": product})
def index(request):
	 return render(request, "test/index.html")
def copy(request):
	 return render(request, "test/copy.html")
# Create your views here.

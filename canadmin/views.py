from django.shortcuts import render
from main.decorators import role_required
from .models import *
# from django.db.models import Sum
from django.http import HttpRequest,HttpResponseForbidden, HttpResponse
from cook.models import *

# Create your views here.
def main_page(request):
    return render(request, "canadmin/main.html")

def vieworders(request: HttpRequest) -> HttpResponse:
    orderdict = Order.objects.all()
    return render(request, 'canadmin/orders.html', context={'orders': orderdict})
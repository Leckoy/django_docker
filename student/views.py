from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from cook.models import dishes

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "student/index.html")

def menu(request: HttpRequest) -> HttpResponse:
    context = {"dishes" : dishes.objects.all()}
    return render(request, "student/menu.html", context)

def allergy(request: HttpRequest) -> HttpResponse:
    pass

def top_up(request: HttpRequest) -> HttpResponse:
    pass

def pay(request: HttpRequest) -> HttpResponse:
    pass
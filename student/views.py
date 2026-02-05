from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from cook.models import Dish
# from cook.models import dishes

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "student/index.html")

def menu(request: HttpRequest) -> HttpResponse:
    context = {"dishes" : Dish.objects.all()}
    return render(request, "student/menu.html", context)

def allergy(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/allergy.html", context)

def top_up(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/top_up.html", context)

def pay_onetime(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/pay_onetime.html", context)

def season_ticket(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/season_ticket.html", context)

def comment(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "student/comment.html", context)
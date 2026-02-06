from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def choice(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "main/choice.html", context)

def registration(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "main/registration.html", context)

def authorization(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "main/authorization.html", context)


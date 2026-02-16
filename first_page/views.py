from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def first_page(request: HttpRequest) -> HttpResponse:
    context={}
    return render(request, "first_page/first.html", context)
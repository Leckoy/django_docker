from django.urls import path
from .views import *

urlpatterns = [
path("", index),
path("products/", fproducts),
path("dishes/", fdishes),
path("Github/", copy),
]
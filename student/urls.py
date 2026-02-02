from django.urls import path
from . import views

urlpatterns = [
    path("main/", views.index, name="main_page"),
    path("menu/", views.menu, name="menu_page"),
    path("allergy/", views.allergy, name="allergy_page"),
    path("top_up/", views.top_up, name="top_up"),
    path("pay/", views.pay, name="pay_page"),
]
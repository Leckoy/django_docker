from django.urls import path
from . import views

urlpatterns = [
    path("choice/", views.choice, name="choice_page"),
    path("registration/", views.registration, name="registration_page"),
    path("authorization/", views.authorization, name="authorization_page")
]
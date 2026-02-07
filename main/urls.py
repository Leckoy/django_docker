from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name="logout"),
    path("choice/", views.choice, name="choice_page"),
    path("registration/", views.registration, name="registration_page"),
    # path("authorization/", views.authorization, name="authorization_page")
]
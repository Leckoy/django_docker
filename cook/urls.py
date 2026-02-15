from django.urls import path
from .views import *
from . import views

urlpatterns = [

path('ingredient/', views.IngredientUse, name='ingredient'),

path('create/', views.CreateMenu, name='create_menu'),

path("dishes/", views.DishAdd, name='dish'),
path("order/", views.IngredientOrder, name='order'),

path("order/", views.IngredientOrder, name='order'),


path('main/', index, name="main_cook_page"),

path('menu/', Menu_view, name="menu")


]
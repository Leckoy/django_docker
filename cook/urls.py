from django.urls import path
from .views import *
from . import views
urlpatterns = [


path('ingredients/', IngredientUseAPI.as_view(), name='ingredient-dashboard'),

path('ingredients/<int:pk>/use/', IngredientUseAPI.as_view(), name='ingredient-use'),

path('dish/<int:pk>', StockCookDishAPI.as_view(), name='cook-dashboard'),

path('stock/<int:pk>/use/', StockCookDishAPI.as_view(), name='dish-cook'),
path('create/', views.CreateMenu, name='create_menu'),



path("products/", fproducts),
path("dishes/", fdishes),

]
from django.urls import path
from .views import *

urlpatterns = [


# path('ingredients/', IngredientUseAPI.as_view(), name='ingredient-dashboard'),

# path('ingredients/<int:pk>/use/', IngredientUseAPI.as_view(), name='ingredient-use'),

# path('dish/<int:pk>', StockCookDishAPI.as_view(), name='cook-dashboard'),

# path('stock/<int:pk>/use/', StockCookDishAPI.as_view(), name='dish-cook'),



path("", index),
path("products/", fproducts),
path("dishes/", fdishes),
path("Github/", copy),
]
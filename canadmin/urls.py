from django.urls import path
from . import views

urlpatterns = [
    # get
    path("", views.main_page, name='admin_main_page'),
    path('view_orders', views.vieworders, name='admin_view_orders'),
    path('statistic', views.statistic, name='statistic'),
    # path('view_log', views.Log, name='view_log')
    # post
    path('orders/change/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path("registration/", views.registration, name="admin_registration_page"),
    path('actions/', views.actions, name='actions'),
    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('ingredients/add', views.ingredadd, name='ingredadd'),

]

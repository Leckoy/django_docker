from django.urls import path
from . import views

urlpatterns = [
    # get
    path("", views.main_page, name='admin_main_page'),
    path('view_orders', views.vieworders, name='admin_view_orders'),
    # path('view_statistic', views.Viewstatistic, name='view_statistic'),
    # path('view_log', views.Log, name='view_log')
    # post
    path('orders/change/<int:order_id>/', views.change_order_status, name='change_order_status'),
    path("registration/", views.registration, name="registration_page"),
    path('actions/', views.actions, name='actions')
]

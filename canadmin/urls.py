from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_page, name='admin_main_page'),
    path('view_orders', views.vieworders, name='admin_view_orders'),
    # path('view_statistic', views.Viewstatistic, name='view_statistic'),
    # path('view_log', views.Log, name='view_log')
]

from django.urls import path
from . import views
urlpatterns = [
    path("main/", views.index, name="main_page"),
    path("menu/", views.Menu_view, name="menu_page"),
    path("allergy/", views.allergy, name="allergy_page"),
    path("allergy/delete/<int:allergy_id>/", views.allergy_delete, name="allergy_delete"),
    path("top_up/", views.top_up, name="top_up"),
    path("pay_onetime/", views.pay_onetime, name="pay_onetime_page"),

    path("comment/<int:dish_id>/", views.FeedBack, name="comment_page"),
    path('orders/daily/', views.my_purchases_list, name='student_orders_page'),
    path('season_ticket/', views.buy_season_ticket, name='season_ticket_page'),

]

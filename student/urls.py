from django.urls import path
from . import views

urlpatterns = [
    path("main/", views.index, name="main_page"),
    path("menu/", views.menu, name="menu_page"),
    path("allergy/", views.allergy, name="allergy_page"),
    path("top_up/", views.top_up, name="top_up"),
    path("pay_onetime/", views.pay_onetime, name="pay_onetime_page"),
    path("season_ticket/", views.season_ticket, name="season_ticket_page"),

    path("comment/<int:dish_id>/", views.FeedBack, name="comment_page")


]
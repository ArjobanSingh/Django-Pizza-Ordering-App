from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name = "login"),
    path("logout/", views.logout, name="logout"),
    path("main_app/", views.main_app, name="main_app"),
    path("register/", views.register, name="registeration"),
    path("cart/", views.cart, name="cart"),
    path("delete/", views.delete, name="delete" ),
    path("orders/", views.orders, name='orders'),
    path("owner_page/", views.owner_page, name="owner_page")
]

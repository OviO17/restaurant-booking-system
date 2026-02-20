from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("book/", views.book_table, name="book_table"),
    path("my-reservations/", views.my_reservations, name="my_reservations"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("book/", views.book_table, name="book_table"),
    path("my-reservations/", views.my_reservations, name="my_reservations"),
    path(
        "cancel/<int:reservation_id>/",
        views.cancel_reservation,
        name="cancel_reservation",
    ),
    path(
        "edit/<int:reservation_id>/",
        views.edit_reservation,
        name="edit_reservation",
    ),
    path(
        "delete/<int:reservation_id>/",
        views.delete_reservation,
        name="delete_reservation",
    ),
]

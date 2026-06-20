from datetime import time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import ReservationForm
from .models import Client, Reservation, Table
from .views import find_available_table


class ProfileLifecycleTests(TestCase):
    def test_regular_user_receives_client_profile(self):
        user = User.objects.create_user("new-user", password="safe-test-password")
        self.assertTrue(Client.objects.filter(user=user).exists())

    def test_superuser_can_open_booking_page(self):
        admin = User.objects.create_superuser(
            "assessor_admin",
            "assessor@example.com",
            "safe-test-password",
        )
        self.client.force_login(admin)

        response = self.client.get(reverse("book_table"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Book a table")
        self.assertTrue(Client.objects.filter(user=admin).exists())

    def test_signup_populates_the_automatically_created_profile(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "web-user",
                "email": "web-user@example.com",
                "full_name": "Web User",
                "phone": "07123456789",
                "referral_name": "A friend",
                "home_address": "",
                "occupation": "Developer",
                "password1": "a-secure-test-password-47",
                "password2": "a-secure-test-password-47",
            },
        )
        user = User.objects.get(username="web-user")
        profile = Client.objects.get(user=user)
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(profile.full_name, "Web User")
        self.assertEqual(profile.email, "web-user@example.com")
        self.assertEqual(profile.phone, "07123456789")


class ReservationFormTests(TestCase):
    def test_form_uses_date_time_and_number_controls(self):
        form = ReservationForm()
        self.assertEqual(form.fields["date"].widget.input_type, "date")
        self.assertEqual(form.fields["time"].widget.input_type, "time")
        self.assertEqual(form.fields["guests"].widget.input_type, "number")
        self.assertEqual(
            form.fields["date"].widget.attrs["min"],
            timezone.localdate().isoformat(),
        )

    def test_past_date_is_rejected(self):
        form = ReservationForm(
            data={
                "date": timezone.localdate() - timedelta(days=1),
                "time": "18:00",
                "guests": 2,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

    def test_time_outside_opening_hours_is_rejected(self):
        form = ReservationForm(
            data={
                "date": timezone.localdate() + timedelta(days=1),
                "time": "10:00",
                "guests": 2,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("time", form.errors)

    def test_guest_limits_are_enforced(self):
        form = ReservationForm(
            data={
                "date": timezone.localdate() + timedelta(days=1),
                "time": "18:00",
                "guests": 13,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("guests", form.errors)


class ReservationCrudTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("diner", password="safe-test-password")
        self.other_user = User.objects.create_user(
            "other",
            password="safe-test-password",
        )
        self.profile = Client.objects.get(user=self.user)
        self.table = Table.objects.create(table_number=1, capacity=4)
        self.booking_date = timezone.localdate() + timedelta(days=2)
        self.client.force_login(self.user)

    def create_reservation(self, **overrides):
        values = {
            "client": self.profile,
            "table": self.table,
            "date": self.booking_date,
            "time": time(18, 0),
            "guests": 2,
            "status": Reservation.STATUS_CONFIRMED,
        }
        values.update(overrides)
        return Reservation.objects.create(**values)

    def test_user_can_create_reservation(self):
        response = self.client.post(
            reverse("book_table"),
            {"date": self.booking_date, "time": "18:00", "guests": 2},
            follow=True,
        )
        self.assertRedirects(response, reverse("my_reservations"))
        self.assertEqual(Reservation.objects.filter(client=self.profile).count(), 1)

    def test_user_can_view_own_reservation(self):
        reservation = self.create_reservation()
        response = self.client.get(reverse("my_reservations"))
        self.assertContains(response, reservation.date.strftime("%Y"))
        self.assertContains(response, "Delete permanently")

    def test_user_can_edit_reservation_without_competing_with_itself(self):
        reservation = self.create_reservation()
        response = self.client.post(
            reverse("edit_reservation", args=[reservation.pk]),
            {"date": self.booking_date, "time": "18:00", "guests": 3},
        )
        reservation.refresh_from_db()
        self.assertRedirects(response, reverse("my_reservations"))
        self.assertEqual(reservation.guests, 3)
        self.assertEqual(reservation.table, self.table)

    def test_user_can_cancel_reservation(self):
        reservation = self.create_reservation()
        response = self.client.post(
            reverse("cancel_reservation", args=[reservation.pk])
        )
        reservation.refresh_from_db()
        self.assertRedirects(response, reverse("my_reservations"))
        self.assertEqual(reservation.status, Reservation.STATUS_CANCELLED)

    def test_cancelled_reservation_releases_table(self):
        self.create_reservation(status=Reservation.STATUS_CANCELLED)
        available = find_available_table(self.booking_date, time(18, 0), 2)
        self.assertEqual(available, self.table)

    def test_user_can_permanently_delete_reservation(self):
        reservation = self.create_reservation()
        response = self.client.post(
            reverse("delete_reservation", args=[reservation.pk])
        )
        self.assertRedirects(response, reverse("my_reservations"))
        self.assertFalse(Reservation.objects.filter(pk=reservation.pk).exists())

    def test_delete_requires_confirmation_post(self):
        reservation = self.create_reservation()
        response = self.client.get(reverse("delete_reservation", args=[reservation.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Reservation.objects.filter(pk=reservation.pk).exists())

    def test_user_cannot_edit_or_delete_another_users_reservation(self):
        other_profile = Client.objects.get(user=self.other_user)
        reservation = self.create_reservation(client=other_profile)
        edit_response = self.client.get(
            reverse("edit_reservation", args=[reservation.pk])
        )
        delete_response = self.client.post(
            reverse("delete_reservation", args=[reservation.pk])
        )
        self.assertEqual(edit_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
        self.assertTrue(Reservation.objects.filter(pk=reservation.pk).exists())

    def test_user_cannot_cancel_another_users_reservation(self):
        other_profile = Client.objects.get(user=self.other_user)
        reservation = self.create_reservation(client=other_profile)
        response = self.client.post(
            reverse("cancel_reservation", args=[reservation.pk])
        )
        reservation.refresh_from_db()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(reservation.status, Reservation.STATUS_CONFIRMED)

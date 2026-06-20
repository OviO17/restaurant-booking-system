from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ReservationForm, SignUpForm
from .models import Client, Reservation, Table
from .signals import profile_defaults


def home(request):
    return render(request, "bookings/home.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            Client.objects.update_or_create(
                user=user,
                defaults={
                    "full_name": form.cleaned_data["full_name"],
                    "email": form.cleaned_data["email"],
                    "phone": form.cleaned_data["phone"],
                    "referral_name": form.cleaned_data["referral_name"],
                    "home_address": form.cleaned_data["home_address"],
                    "occupation": form.cleaned_data["occupation"],
                },
            )

            login(request, user)
            messages.success(request, "Account created. You are now logged in.")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


def get_client_for_user(user):
    """Return a profile, repairing accounts created before signals were added."""
    client = Client.objects.filter(user=user).first()
    if client:
        return client

    defaults = profile_defaults(user)
    if Client.objects.filter(email=defaults["email"]).exists():
        defaults["email"] = f"{user.username}-{user.pk}@users.local"
    return Client.objects.create(user=user, **defaults)


def find_available_table(date, time, guests, exclude_reservation=None):
    """
    Return the first table with enough seats that is not already confirmed
    for the requested date and time.
    """
    booked = Reservation.objects.filter(
        date=date,
        time=time,
        status=Reservation.STATUS_CONFIRMED,
    )
    if exclude_reservation:
        booked = booked.exclude(pk=exclude_reservation.pk)

    return Table.objects.filter(capacity__gte=guests).exclude(
        pk__in=booked.values("table_id")
    ).order_by("capacity", "table_number").first()


@login_required
def book_table(request):
    client = get_client_for_user(request.user)

    if request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid():
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            guests = form.cleaned_data["guests"]

            table = find_available_table(date, time, guests)

            if not table:
                form.add_error(
                    None,
                    "No tables available for that date/time and party size.",
                )
            else:
                Reservation.objects.create(
                    client=client,
                    table=table,
                    date=date,
                    time=time,
                    guests=guests,
                    status=Reservation.STATUS_CONFIRMED,
                )
                messages.success(request, f"Booking confirmed! You got {table}.")
                return redirect("my_reservations")
    else:
        form = ReservationForm()

    return render(request, "bookings/book_table.html", {"form": form})


@login_required
def my_reservations(request):
    client = get_client_for_user(request.user)
    reservations = Reservation.objects.filter(client=client).order_by(
        "-date",
        "-time",
    )

    return render(
        request,
        "bookings/my_reservations.html",
        {"reservations": reservations},
    )


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        client__user=request.user,
    )

    if request.method == "POST":
        reservation.status = Reservation.STATUS_CANCELLED
        reservation.save()
        messages.success(request, "Reservation cancelled successfully.")

    return redirect("my_reservations")


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        client__user=request.user,
    )

    if reservation.status == Reservation.STATUS_CANCELLED:
        messages.error(request, "You cannot edit a cancelled reservation.")
        return redirect("my_reservations")

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)

        if form.is_valid():
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            guests = form.cleaned_data["guests"]

            table = find_available_table(
                date,
                time,
                guests,
                exclude_reservation=reservation,
            )

            if not table:
                form.add_error(None, "No tables available.")
            else:
                reservation.date = date
                reservation.time = time
                reservation.guests = guests
                reservation.table = table
                reservation.save()

                messages.success(request, "Reservation updated!")
                return redirect("my_reservations")
    else:
        form = ReservationForm(instance=reservation)

    return render(request, "bookings/edit_reservation.html", {"form": form})

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        client__user=request.user,
    )

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Reservation deleted successfully.")
        return redirect("my_reservations")

    return render(
        request,
        "bookings/delete_reservation.html",
        {"reservation": reservation},
    )

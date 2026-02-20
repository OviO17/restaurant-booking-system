from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import SignUpForm, ReservationForm
from .models import Client, Table, Reservation


def home(request):
    return render(request, "bookings/home.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()

            Client.objects.create(
                user=user,
                full_name=form.cleaned_data["full_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                referral_name=form.cleaned_data["referral_name"],
                home_address=form.cleaned_data["home_address"],
                occupation=form.cleaned_data["occupation"],
            )

            login(request, user)
            messages.success(request, "Account created. You are now logged in.")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


def find_available_table(date, time, guests):
    """
    Returns the first table with enough capacity that is not already booked
    at the requested date/time.
    """
    return (
        Table.objects.filter(capacity__gte=guests)
        .exclude(
            reservations__date=date,
            reservations__time=time,
            reservations__status=Reservation.STATUS_CONFIRMED,
        )
        .order_by("capacity", "table_number")
        .first()
    )


@login_required
def book_table(request):
    client = Client.objects.filter(user=request.user).first()
    if not client:
        messages.error(request, "Please complete signup before booking.")
        return redirect("signup")

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            time = form.cleaned_data["time"]
            guests = form.cleaned_data["guests"]

            if date < timezone.localdate():
                form.add_error("date", "Please choose a future date.")
            else:
                table = find_available_table(date, time, guests)
                if not table:
                    form.add_error(None, "No tables available for that date/time and party size.")
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
    client = Client.objects.filter(user=request.user).first()
    reservations = Reservation.objects.filter(client=client).order_by("-date", "-time")
    return render(request, "bookings/my_reservations.html", {"reservations": reservations})
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Reservation


class SignUpForm(UserCreationForm):
    """Create both the Django user and the restaurant profile details."""

    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    referral_name = forms.CharField(max_length=100, required=False)
    home_address = forms.CharField(max_length=200, required=False)
    occupation = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "full_name",
            "phone",
            "referral_name",
            "home_address",
            "occupation",
            "password1",
            "password2",
        )

    def clean_email(self):
        """Prevent a signup from reusing an existing account email."""
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class ReservationForm(forms.ModelForm):
    """Validate a reservation and render unambiguous booking controls."""

    class Meta:
        model = Reservation
        fields = ["date", "time", "guests"]
        help_texts = {
            "date": "Choose today or a future date.",
            "time": "Choose an available time between 12:00 and 22:00.",
            "guests": "Bookings are available for 1 to 12 guests.",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "time": forms.TimeInput(
                attrs={"type": "time", "min": "12:00", "max": "22:00", "step": "1800"},
                format="%H:%M",
            ),
            "guests": forms.NumberInput(attrs={"min": 1, "max": 12, "step": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget.attrs["min"] = timezone.localdate().isoformat()

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date < timezone.localdate():
            raise forms.ValidationError("Choose today or a future date.")
        return date

    def clean_time(self):
        booking_time = self.cleaned_data["time"]
        opening = booking_time.replace(hour=12, minute=0, second=0, microsecond=0)
        closing = booking_time.replace(hour=22, minute=0, second=0, microsecond=0)
        if not opening <= booking_time <= closing:
            raise forms.ValidationError("Choose a time between 12:00 and 22:00.")
        return booking_time

    def clean_guests(self):
        guests = self.cleaned_data["guests"]
        if not 1 <= guests <= 12:
            raise forms.ValidationError("Bookings are available for 1 to 12 guests.")
        return guests

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        booking_time = cleaned_data.get("time")
        if date == timezone.localdate() and booking_time:
            local_now = timezone.localtime()
            if booking_time <= local_now.time():
                self.add_error("time", "Choose a time later than the current time.")
        return cleaned_data

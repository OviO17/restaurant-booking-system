from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Reservation


class SignUpForm(UserCreationForm):
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


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["date", "time", "guests"]

    def clean_date(self):
        date = self.cleaned_data["date"]

        # Prevent booking in the past
        if date < timezone.localdate():
            raise forms.ValidationError("You cannot book a past date.")

        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        # Prevent booking earlier today (past time)
        if date == timezone.localdate() and time:
            now_time = timezone.now().time()
            if time < now_time:
                raise forms.ValidationError("You cannot book a past time.")

        return cleaned_data

    def clean_guests(self):
        guests = self.cleaned_data["guests"]

        if guests < 1:
            raise forms.ValidationError("At least 1 guest required.")

        if guests > 12:
            raise forms.ValidationError("Maximum 12 guests allowed.")

        return guests
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

    def clean_guests(self):
        guests = self.cleaned_data["guests"]
        if guests < 1 or guests > 12:
            raise forms.ValidationError("Guest number must be between 1 and 12.")
        return guests
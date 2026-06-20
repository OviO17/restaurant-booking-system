class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["date", "time", "guests"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "guests": forms.NumberInput(attrs={"min": 1, "max": 12}),
        }

    def clean_date(self):
        date = self.cleaned_data["date"]

        if date < timezone.localdate():
            raise forms.ValidationError("You cannot book a past date.")

        return date

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

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
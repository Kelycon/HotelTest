from django import forms
from .models import Booking


class BookingCreateForm(forms.ModelForm):
    observations = forms.CharField(required=False, max_length=200)

    class Meta:
        model = Booking
        exclude = (
            "created_date", "updated_date", "code", "total"
        )

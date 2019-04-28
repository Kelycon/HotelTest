from django import forms


class FindAvailabilityListForm(forms.Form):
    guest = forms.IntegerField(required=True)
    checkin = forms.DateField(required=True, widget=forms.DateInput())
    checkout = forms.DateField(required=True, widget=forms.DateInput())

    def clean(self):
        cleaned_data = super(FindAvailabilityListForm, self).clean()

        checkin = cleaned_data.get('checkin')
        checkout = cleaned_data.get('checkout')

        if checkin > checkout:
            raise forms.ValidationError("La fecha de ingreso no puede ser mayor a la de salida!")

        return cleaned_data

# -*- coding: utf-8 -*-
import datetime
from django import forms


class FindAvailabilityListForm(forms.Form):
    guest = forms.IntegerField(required=True)
    checkin = forms.DateField(required=True, widget=forms.DateInput())
    checkout = forms.DateField(required=True, widget=forms.DateInput())

    def clean(self):
        cleaned_data = super(FindAvailabilityListForm, self).clean()

        checkin = cleaned_data.get('checkin')
        checkout = cleaned_data.get('checkout')

        start_year = datetime.datetime.strptime('2019-01-01', "%Y-%m-%d").date()
        end_year = datetime.datetime.strptime('2019-12-31', "%Y-%m-%d").date()

        if checkin > checkout:
            raise forms.ValidationError("La fecha de ingreso no puede ser mayor a la de salida!")

        if checkin > end_year:
            raise forms.ValidationError("La fecha de ingreso máxima es 2019-12-31!")

        if checkout > end_year:
            raise forms.ValidationError("La fecha de salida máxima es 2019-12-31!")

        if checkin < start_year:
            raise forms.ValidationError("La fecha de ingreso mínima es 2019-01-01!")

        if checkout < start_year:
            raise forms.ValidationError("La fecha de salida mínima es 2019-01-01!")

        if checkin == checkout:
            raise forms.ValidationError("La fecha para reservar debe ser de por lo menos 1 día!")

        return cleaned_data

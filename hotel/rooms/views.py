# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import F, Case, IntegerField, When, Q, Count
from .models import Room
from bookings.models import Booking
from .forms import FindAvailabilityListForm


def home(request):
    return render(request, 'home.html')


class FindAvailability(ListView):
    model = Room
    paginate_by = 100
    context_object_name = 'room_list'
    template_name = 'results.html'

    def dispatch(self, request):
        self.filter_form = FindAvailabilityListForm(self.request.GET)
        return super(FindAvailability, self).dispatch(request=request)

    def get(self, request, *args, **kwargs):
        if self.filter_form.has_changed() and not self.filter_form.is_valid():
            return self.form_invalid()
        return super(FindAvailability, self).get(request, *args, **kwargs)

    def get_queryset(self):
        checkin = self.filter_form.cleaned_data.get('checkin')
        checkout = self.filter_form.cleaned_data.get('checkout')
        guest = self.filter_form.cleaned_data.get('guest')
        booking_days = (checkout - checkin).days

        filter_booking_date_1 = Q(Q(Q(check_in__lte=checkin),  Q(check_in__lte=checkout)),
                                  Q(Q(check_out__lte=checkout),  Q(check_out__gte=checkin)))
        filter_booking_date_2 = Q(Q(Q(check_in__lte=checkin),  Q(check_in__lte=checkout)),
                                  Q(Q(check_out__gte=checkout),  Q(check_out__gte=checkin)))
        filter_booking_date_3 = Q(Q(Q(check_in__gte=checkin),  Q(check_out__lte=checkout)),
                                  Q(Q(check_out__gte=checkout),  Q(check_out__gte=checkin)))
        filter_booking_date_4 = Q(Q(Q(check_in__gte=checkin),  Q(check_out__lte=checkout)),
                                  Q(Q(check_out__lte=checkin),  Q(check_out__gte=checkin)))

        filter_booking = Q(filter_booking_date_1 | filter_booking_date_2 | filter_booking_date_3 | filter_booking_date_4)

        # Count bookings for room type
        bookings = Booking.objects.filter(filter_booking, room__guest__gte=guest).values('room__type').annotate(
                availability=Count('code')
            )

        # Get rooms by guest
        rooms = Room.objects.filter(guest__gte=guest).annotate(
                price=F('value') * booking_days
            )

        # Update rooms with real availability
        for room in rooms:
            for booking in bookings:
                if room.code == booking.get('room__type'):
                    room.availability = room.availability - booking.get('availability')

        return rooms

    def get_context_data(self, **kwargs):
        context = super(FindAvailability, self).get_context_data(**kwargs)
        return context

    def form_invalid(self):
        return render(self.request, 'home.html', {'form': self.filter_form})

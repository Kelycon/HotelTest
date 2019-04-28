# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import F, Case, IntegerField, When, Q, Count
from .models import Room
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

        filter_booking = Q(Q(Q(booking__check_in__gte=checkin), Q(booking__check_out__lte=checkout)) | Q(booking__code__isnull=True))

        rooms = Room.objects.filter(
            filter_booking, guest__gte=guest
        ).values('type', 'guest', 'file', 'code').order_by('guest').annotate(
            availability=F('availability') - Case(
                    When(booking__code__isnull=False, then=Count('booking__code')),
                    default=0,
                    output_field=IntegerField()
            ),
            price=F('value') * booking_days
        )
        import ipdb; ipdb.set_trace()
        return rooms

    def get_context_data(self, **kwargs):
        context = super(FindAvailability, self).get_context_data(**kwargs)
        return context

    def form_invalid(self):
        return render(self.request, 'home.html', {'form': self.filter_form})

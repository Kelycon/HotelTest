# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from retools.lock import Lock, LockTimeout
from .models import Booking
from rooms.models import Room
from django.contrib.auth.models import User
from rooms.forms import FindAvailabilityListForm
from django.contrib import messages
from .forms import (
    BookingCreateForm, BookingUpdateForm
)


class BookingCreate(CreateView):
    model = Booking
    form_class = BookingCreateForm

    @method_decorator(login_required)
    def dispatch(self, request, pk):
        return super(BookingCreate, self).dispatch(request=request, pk=pk)

    def get(self, request, pk):
        # Validate get parameter
        filter_form = FindAvailabilityListForm(request.GET)
        if filter_form.has_changed() and not filter_form.is_valid():
            return render(request, 'home.html', {'error': 'Ha ocurrido un error inesperado. Intentelo de nuevo.'})
        else:
            checkin = filter_form.cleaned_data.get('checkin')
            checkout = filter_form.cleaned_data.get('checkout')

            # Return correct view
            return self.get_view(pk, checkin, checkout, self.form_class)

    def post(self, request, pk, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, pk)

    def form_valid(self, form):
        lock_counter_key = 'LOCK_COUNTER_KEY'
        try:
            # Semaphore to prevent overbooking
            with Lock(lock_counter_key, expires=120, timeout=120):
                self.object = form.save(commit=False)

                # Can booking this room?
                if not self.exist_availability(self.object.check_in, self.object.check_out, self.object.room):
                    return render(
                            self.request,
                            'home.html',
                            {
                                'error': 'No existe disponibildad para esta habitación en el rango de fechas seleccionado.'
                            })

                # Generate unique booking code
                code = self.get_unique_code()

                self.object.code = code
                self.object.user = self.request.user
                self.object.total = self.get_total_booking(self.object.check_in, self.object.check_out, self.object.room.value)

                self.object.save()

                messages.add_message(self.request, messages.SUCCESS, 'Tu reserva se ha guardado satisfactoriamente.')

                return redirect('booking-detail', pk=self.object.code)
        except LockTimeout:
            return render(self.request, 'home.html', {'error': 'Ha ocurrido un error inesperado. Intentelo de nuevo.'})

    def exist_availability(self, checkin, checkout, room):
        # Validate if exist room
        filter_booking_date_1 = Q(Q(Q(check_in__lte=checkin),  Q(check_in__lte=checkout)),
                                  Q(Q(check_out__lte=checkout),  Q(check_out__gte=checkin)))
        filter_booking_date_2 = Q(Q(Q(check_in__lte=checkin),  Q(check_in__lte=checkout)),
                                  Q(Q(check_out__gte=checkout),  Q(check_out__gte=checkin)))
        filter_booking_date_3 = Q(Q(Q(check_in__gte=checkin),  Q(check_out__lte=checkout)),
                                  Q(Q(check_out__gte=checkout),  Q(check_out__gte=checkin)))
        filter_booking_date_4 = Q(Q(Q(check_in__gte=checkin),  Q(check_out__lte=checkout)),
                                  Q(Q(check_out__lte=checkin),  Q(check_out__gte=checkin)))

        filter_booking = Q(filter_booking_date_1 | filter_booking_date_2 | filter_booking_date_3 | filter_booking_date_4)

        # Get bookins for dates and room type
        bookings_amout = Booking.objects.filter(
                filter_booking, room_id=room.code
            ).count()

        # Compare with room availability
        if bookings_amout >= room.availability:
            return False

        return True

    def form_invalid(self, form, pk):
        checkin = form.cleaned_data.get('check_in')
        checkout = form.cleaned_data.get('check_out')

        return self.get_view(pk, checkin, checkout, form)

    def get_view(self, pk, checkin, checkout, form):
        # Get Room instance
        room = self.get_room(pk)

        # If data is incomplete return error
        if not checkin or not checkout or not room:
            return render(self.request, 'home.html', {'error': 'Ha ocurrido un error inesperado. Intentelo de nuevo.'})

        context = {
            'form': form,
            'room': room,
            'price': self.get_total_booking(checkin, checkout, room.value)
        }

        return render(self.request, 'booking-create.html', context)

    def get_room(self, pk):
        room = ''

        try:
            room = Room.objects.get(code=pk)
        except Exception as e:
            return False

        return room

    def get_unique_code(self):
        allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567889"
        code = User.objects.make_random_password(length=20, allowed_chars=allowed_chars)

        if Booking.objects.filter(code=code).exists():
            return self.get_unique_code()

        return code

    def get_total_booking(self, checkin, checkout, value):
        booking_days = (checkout - checkin).days

        return value * booking_days


class BookingDetail(DetailView):
    model = Booking
    template_name = 'booking-detail.html'
    context_object_name = 'booking'

    @method_decorator(login_required)
    def dispatch(self, request, pk):
        return super(BookingDetail, self).dispatch(request=request)

    def get_context_data(self, **kwargs):
        context = super(BookingDetail, self).get_context_data(**kwargs)
        context['bookings'] = self.get_bookings()
        return context

    def get_bookings(self):
        return Booking.objects.filter(user_id=self.request.user.id).exclude(code=self.kwargs.get('pk'))


class BookingList(ListView):
    model = Booking
    template_name = 'booking-list.html'
    context_object_name = 'bookings'

    @method_decorator(login_required)
    def dispatch(self, request):
        return super(BookingList, self).dispatch(request=request)

    def get_queryset(self):
        return Booking.objects.filter(user_id=self.request.user.id)


class BookingUpdate(UpdateView):
    model = Booking
    form_class = BookingUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, pk):
        return super(BookingUpdate, self).dispatch(request=request)

    def get_success_url(self):
        return reverse("booking-detail", kwargs={'pk': self.kwargs.get('pk')})

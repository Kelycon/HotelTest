# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from hotel.test_base import TestBase
from .models import Booking
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class BookingTests(TestBase):

    def test_booking_create(self):
        print('test_booking_create')

        signin = {
            'username': self.user.username,
            'password': self.password
        }
        self.signin(signin)

        self.assertEquals(
            Booking.objects.all().count(), 0
        )

        data = {
            'room': self.simple_room.code,
            'name': 'rub',
            'last_name': 'nog',
            'phone': '123',
            'email': '123@123.com',
            'check_in': '2019-04-29',
            'check_out': '2019-04-30',
            'observations': 'qwerty',
            'card_payment_holder': 'rub nog',
            'card_payment_type': Booking.DINNERS_CLUB,
            'card_payment_number': '12345',
            'card_payment_expiration_month': '12',
            'card_payment_expiration_year': '3498',
            'card_payment_cvc': '23'
        }

        self.client.post(
                reverse('booking-create', kwargs={'pk': self.simple_room.code}), data)

        self.assertEquals(
            Booking.objects.all().count(), 1
        )

        self.assertTrue(
            Booking.objects.filter(check_in=data.get('check_in'), check_out=data.get('check_out')).exists()
        )

    def test_booking_update(self):
        print('test_booking_update')

        signin = {
            'username': self.user.username,
            'password': self.password
        }
        self.signin(signin)

        checkin = datetime.datetime.now()
        checkout = checkin + datetime.timedelta(days=4)
        allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567889"

        booking = Booking(
                code=User.objects.make_random_password(length=20, allowed_chars=allowed_chars), user=self.user,
                room=self.double_room, check_in=checkin, check_out=checkout, name='Rub', last_name='Nog', phone='123',
                email='rub@rub.com', observations='Texto', card_payment_holder='RubNog', card_payment_type=Booking.VISA,
                card_payment_number='098', card_payment_expiration_year='2019', card_payment_expiration_month=12,
                card_payment_cvc='1234'
            )

        booking.save()

        self.assertEquals(
            Booking.objects.all().count(), 1
        )

        data = {
            'name': 'rub',
            'last_name': 'nog',
            'phone': '123',
            'email': '123@123.com',
            'observations': 'qwerty',
            'card_payment_holder': 'rub nog',
            'card_payment_type': Booking.DINNERS_CLUB,
            'card_payment_number': '12345',
            'card_payment_expiration_month': '12',
            'card_payment_expiration_year': '3498',
            'card_payment_cvc': '23'
        }

        self.client.post(
                reverse('booking-update', kwargs={'pk': booking.code}), data)

        self.assertEquals(
            Booking.objects.all().count(), 1
        )

        self.assertTrue(
            Booking.objects.filter(card_payment_number=data.get('card_payment_number'), email=data.get('email')).exists()
        )

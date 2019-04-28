
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from hotel.test_base import TestBase
from django.core.urlresolvers import reverse
from bookings.models import Booking
from django.contrib.auth.models import User


class RoomsTests(TestBase):

    def test_find_availability(self):
        print('test_find_availability')

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

        data = {
            'checkin': checkin.strftime('%Y-%m-%d'),
            'checkout': checkout.strftime('%Y-%m-%d'),
            'guest': 1
        }

        response = self.client.get(
                reverse('availability'), data)

        self.assertEquals(response.status_code, 200)

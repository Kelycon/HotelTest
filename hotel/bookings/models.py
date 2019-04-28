# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room


class Booking(models.Model):
    VISA = 'V'
    MASTER_CARD = 'MC'
    AMERICAN_EXPRESS = 'AE'
    DINNERS_CLUB = 'DC'

    CardTypes = (
        (VISA, 'VISA'),
        (MASTER_CARD, 'MASTER CARD'),
        (AMERICAN_EXPRESS, 'AMERICAN EXPRESS'),
        (DINNERS_CLUB, 'DINNERS CLUB')
    )

    code = models.CharField("Código reserva", max_length=18, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    room = models.ForeignKey(Room,  on_delete=models.PROTECT)
    check_in = models.DateField("Fecha entrada")
    check_out = models.DateField("Fecha salida")
    total = models.DecimalField("Total", max_digits=18, decimal_places=2, default=0)
    name = models.CharField("Nombre", max_length=50)
    last_name = models.CharField("Apellidos", max_length=50)
    phone = models.CharField("Teléfono", max_length=20)
    email = models.CharField("Email", max_length=50)
    observations = models.CharField("Observaciones", max_length=200, null=True)
    card_payment_holder = models.CharField("Titular tarjeta", max_length=100)
    card_payment_type = models.CharField("Tipo tarjeta",  max_length=4, default=VISA, choices=CardTypes)
    card_payment_number = models.CharField("Tarjeta número", max_length=20)
    card_payment_expiration_month = models.IntegerField("Tarjeta mes caducidad")
    card_payment_expiration_year = models.IntegerField("Tarjeta año caducidad")
    card_payment_cvc = models.CharField("CVC", max_length=4)

    created_date = models.DateTimeField("Fecha creación", editable=False)
    updated_date = models.DateTimeField("Fecha actualización", null=True, editable=False)

    class Meta:
        db_table = 'RESERVAS'
        verbose_name = 'Reserva'

    def __str__(self):
        return str(self.code)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.created_date:
            self.created_date = datetime.datetime.today()
        self.updated_date = datetime.datetime.today()
        return super(Booking, self).save(*args, **kwargs)

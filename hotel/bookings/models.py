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

    code = models.CharField(db_column='CODIGO_RESERVA', max_length=18, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    room = models.ForeignKey(Room,  on_delete=models.PROTECT, db_column='HABITACION_ID')
    check_in = models.DateField(db_column='FECHA_ENTRADA')
    check_out = models.DateField(db_column='FECHA_SALIDA')
    total = models.DecimalField("total", db_column='VALOR_TOTAL', max_digits=18, decimal_places=2, default=0)
    name = models.CharField(db_column='NOMBRE', max_length=50)
    last_name = models.CharField(db_column='APELLIDO', max_length=50)
    phone = models.CharField(db_column='TELEFONO', max_length=20)
    email = models.CharField(db_column='EMAIL', max_length=50)
    observations = models.CharField(db_column='OBSERVACIONES', max_length=200, null=True)
    card_payment_holder = models.CharField(db_column='TITULAR_TARJETA', max_length=100)
    card_payment_type = models.CharField(
            db_column='TARJETA_TIPO', max_length=4, default=VISA, choices=CardTypes)
    card_payment_number = models.CharField(db_column='TARJETA_NUMERO', max_length=20)
    card_payment_expiration_month = models.IntegerField(db_column='TARJETA_MES_CADUCIDAD')
    card_payment_expiration_year = models.IntegerField(db_column='TARJETA_AÑO_CADUCIDAD')
    card_payment_cvc = models.CharField(db_column='TARJETA_CVC', max_length=4)

    created_date = models.DateTimeField(db_column='FECHA_CREA', editable=False)
    updated_date = models.DateTimeField(db_column='FECHA_MODIFICA', null=True, editable=False)

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

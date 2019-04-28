# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Room(models.Model):
    SIMPLE = 1
    DOUBLE = 2
    TRIPLE = 3
    QUADRUPLE = 4

    RoomTypes = (
        (SIMPLE, 'Individual'),
        (DOUBLE, 'Doble'),
        (TRIPLE, 'Triple'),
        (QUADRUPLE, 'Cuadruple')
    )

    code = models.AutoField("Código habitación", primary_key=True)
    type = models.IntegerField("Tipo", default=SIMPLE, choices=RoomTypes, unique=True)
    guest = models.IntegerField("Máximo personas")
    # Cantidad de habitaciones disponibles
    availability = models.IntegerField("Disponibles", default=0)
    value = models.DecimalField("Valor por día", max_digits=18, decimal_places=2)
    file = models.FileField(
        "Foto", upload_to='uploads', blank=True, null=True)

    class Meta:
        db_table = 'HABITACIONES'
        verbose_name = 'Habitacion'
        verbose_name_plural = "Habitaciones"

    def __str__(self):
        return str(self.type)

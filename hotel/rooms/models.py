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

    code = models.AutoField(db_column='HABITACION_ID', primary_key=True)
    type = models.IntegerField("Tipo", db_column='TIPO_HABITACION', default=SIMPLE, choices=RoomTypes, unique=True)
    guest = models.IntegerField("Máximo personas", db_column='MAXIMO_PERSONAS')
    # Cantidad de habitaciones disponibles
    availability = models.IntegerField("Disponibles", db_column='DISPONIBILIDAD', default=0)
    value = models.DecimalField("Valor por día", db_column='VALOR_DIA', max_digits=18, decimal_places=2)
    file = models.FileField(
        "Foto", upload_to='uploads', blank=True, null=True, db_column='FILE')

    class Meta:
        db_table = 'HABITACIONES'
        verbose_name = 'Habitacion'
        verbose_name_plural = "Habitaciones"

    def __str__(self):
        return str(self.type)

# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-28 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_room_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='availability',
            field=models.IntegerField(default=0, verbose_name='Disponibles'),
        ),
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='C\xf3digo habitaci\xf3n'),
        ),
        migrations.AlterField(
            model_name='room',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='room',
            name='guest',
            field=models.IntegerField(verbose_name='M\xe1ximo personas'),
        ),
        migrations.AlterField(
            model_name='room',
            name='type',
            field=models.IntegerField(choices=[(1, 'Individual'), (2, 'Doble'), (3, 'Triple'), (4, 'Cuadruple')], default=1, unique=True, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='room',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Valor por d\xeda'),
        ),
    ]
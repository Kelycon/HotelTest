# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-27 17:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20190427_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='file',
            field=models.FileField(blank=True, db_column='FILE', null=True, upload_to='uploads', verbose_name='Foto'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Booking
from rooms.models import Room


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('code', 'check_in', 'check_out', 'total', 'phone', 'email', 'get_room_display')

    def get_room_display(self, obj):
        return obj.room.get_type_display()

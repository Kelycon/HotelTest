from django import template
from rooms.models import Room
from hotel.settings import SITE_URL, MEDIA_URL

register = template.Library()


@register.filter
def get_room_name(value):
    return dict(Room.RoomTypes).get(value)


@register.filter
def get_url_file(value):
    return SITE_URL + MEDIA_URL + value

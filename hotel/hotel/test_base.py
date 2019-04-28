import json
from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from rooms.models import Room


class TestBase(TransactionTestCase):

    password = '1234'

    def setUp(self):
        self.user = User.objects.create_user(username='Ruben', email='ruben@test.com', password=self.password)

        self.simple_room = Room(type=Room.SIMPLE, guest=1, value=20, availability=10)
        self.simple_room.save()

        self.double_room = Room(type=Room.DOUBLE, guest=2, value=30, availability=5)
        self.double_room.save()

        self.triple_room = Room(type=Room.TRIPLE, guest=3, value=40, availability=20)
        self.triple_room.save()

        self.quadruple_room = Room(type=Room.QUADRUPLE, guest=4, value=50, availability=4)
        self.quadruple_room.save()

    def signin(self, data):
        response = self.client.post(reverse('signin-user'), {
            'username': data.get('username'),
            'password': data.get('password')
        })
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(content.get('success'))
        return content

    def signout(self):
        response = self.client.post(reverse('signout-user'))
        self.assertEquals(response.status_code, 200)
        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(content.get('success'))
        return content

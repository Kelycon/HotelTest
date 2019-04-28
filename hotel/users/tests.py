# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from hotel.test_base import TestBase
from django.contrib.auth.models import User


class UsersTests(TestBase):

    def test_signin(self):
        print('test_signin')

        data = {
            'username': self.user.username,
            'password': self.password
        }

        self.signin(data)

    def test_signup(self):
        print('test_signup')

        data = {
            'username': 'Rubenxuz',
            'password1': 'nuevo1234',
            'password2': 'nuevo1234',
            'email': 'rub@rub.com'
        }

        self.client.post(reverse('signup-user'), data)

        self.assertTrue(
            User.objects.filter(username=data.get('username'), email=data.get('email')).exists()
        )

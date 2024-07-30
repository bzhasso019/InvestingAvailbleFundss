import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from app.scripts.funcs import returnJson
from app.scripts.authorisation.login import authorisationBack
import json

class AuthorisationBackTest(TestCase):

    def setUp(self):
        # пользователь для тестирования
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()

    def test_authorisation_success(self):
        response = self.client.post('/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode())
        #пустое сообщение окей, пустое сообщение
        self.assertEqual(response_data, {'status': 'success','message':''})

    def test_authorisation_failure(self):
        response = self.client.post('/login/', {'username': self.username, 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode())
        self.assertEqual(response_data, {'status': 'Error', 'message': 'Неверный логин или пароль'})


    def test_authorisation_no_credentials(self):
        response = self.client.post('/login/', {})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content.decode())
        self.assertEqual(response_data, {'status': 'Error', 'message': 'Неверный логин или пароль'})

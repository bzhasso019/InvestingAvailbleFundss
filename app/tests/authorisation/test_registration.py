import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.scripts.funcs import returnJson
from app.scripts.authorisation.registration import registrationBack
import json

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            first_name='Test',
            last_name='User',
            email='test@example.com'
        )
#ant
    def test_registration_success(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'testpass123',
            'name': 'Test User2',
            'email': 'test2@example.com',
            'phone': '89123456788',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('status', response_data)
        self.assertEqual(response_data['status'], 'success')
        self.assertTrue(User.objects.filter(username='testuser2').exists())
#ant
    def test_registration_fail_empty_role(self):
        response = self.client.post('/reg/', {
            'role': ' ',
            'login': 'testuser2',
            'password': 'testpass123',
            'name': 'Test User',
            'email': 'test2@example.com',
            'phone': '89125456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('role', response_data)
        self.assertEqual(response_data['role'], 'Роль введена некорректно')
#ant
    def test_registration_fail_short_password(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'short',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('password', response_data)
        self.assertEqual(response_data['password'], 'Пароль слишком короткий')
#ant
    def test_registration_fail_short_empty(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': '',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('password', response_data)
        self.assertEqual(response_data['password'], 'Пароль слишком короткий')
#ant
    def test_registration_fail_bad_password(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'short!@(#@#_$(^',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('password', response_data)
        self.assertEqual(response_data['password'], 'Пароль имеет недопустимые символы')
#ant
    def test_registration_fail_invalid_email(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'testpass123',
            'name': 'Test User',
            'email': 'invalid-email',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('email', response_data)
        self.assertEqual(response_data['email'], 'Введите корректную почту')
#ant
    def test_registration_fail_long_email(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'testpass123',
            'name': 'Test User',
            'email': 'a'*150+'@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('email', response_data)
        self.assertEqual(response_data['email'], 'Почта слишком длинная')

    def test_registration_fail_empty_email(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'testpass123',
            'name': 'Test User',
            'email': ' ',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('email', response_data)
        self.assertEqual(response_data['email'], 'Введите корректную почту')

    def test_registration_fail_empty_phone(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('phone', response_data)
        self.assertEqual(response_data['phone'], 'Телефон введён некорректно')
#ant
    def test_registration_fail_long_phone(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '891234567812323',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('phone', response_data)
        self.assertEqual(response_data['phone'], 'Телефон введён некорректно')

    def test_registration_fail_long_fio(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': 'Test' * 160 + ' User',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('name', response_data)
        self.assertEqual(response_data['name'], 'ФИО слишком длинное')

    def test_registration_fail_empty_fio(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': '',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('name', response_data)
        self.assertEqual(response_data['name'], 'ФИО введён некорректно')

    def test_registration_fail_fio_incorrect(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': 'Test',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('name', response_data)
        self.assertEqual(response_data['name'], 'ФИО введён некорректно')

    def test_existing_user(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser',
            'password': 'testpass123',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('email', response_data)
        self.assertEqual(response_data['email'], 'Пользователь уже существует')
#ant
    def test_registration_fail_long_address(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'A'* 151,
            'title': 'Test Title',
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('address', response_data)
        self.assertEqual(response_data['address'], 'Адрес слишком длинный')

    def test_registration_long_title(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title' * 150,
            'typeProperty': 'Test Property'
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('title', response_data)
        self.assertEqual(response_data['title'], 'Название организации слишком длинное')

    def test_registration_fail_empty_typeProperty(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': ' '
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('typeProperty', response_data)
        self.assertEqual(response_data['typeProperty'], 'Введите тип собственности')

    def test_registration_fail_long_typeProperty(self):
        response = self.client.post('/reg/', {
            'role': 'Manager',
            'login': 'testuser2',
            'password': 'shortssss',
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '89123456789',
            'address': 'Test Address',
            'title': 'Test Title',
            'typeProperty': 'Test Property' * 50
        })

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('typeProperty', response_data)
        self.assertEqual(response_data['typeProperty'], 'Тип собственности слишком длинный')
        #fdfsdf
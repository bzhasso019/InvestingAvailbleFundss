'''import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db import connection
from app.scripts.clientProfile import private_profile

class PrivateProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.client.login(username='testuser', password='testpass123')

        # Создание необходимых записей в таблицах
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Enterprises")
            cursor.execute("DELETE FROM Users")
            cursor.execute("DELETE FROM auth_user")

            cursor.execute("ALTER SEQUENCE enterprises_id_enterprise_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE users_id_user_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE auth_user_id_seq RESTART WITH 1")

            cursor.execute("INSERT INTO Enterprises (id_enterprise, title, typeProperty, address, phone) VALUES (1, 'Test Enterprise', 'Private', '123 Test St', '1234567890')")
            cursor.execute(f"INSERT INTO Users (id_user, id_employee, id_enterprise) VALUES (1, NULL, 1)")
            cursor.execute(f"INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, id_user) VALUES (1, 'pbkdf2_sha256$260000$XXXX', NULL, FALSE, 'testuser', 'Test', 'User', 'test@example.com', FALSE, TRUE, '2023-01-01', 1)")

    def test_private_profile(self):
        request = self.client.get('/')
        request.user = self.user
        profile_data = private_profile(request)

        expected_data = {
            'email': 'test@example.com',
            'name': 'User Test',
            'phone': '1234567890',
            'address': '123 Test St'
        }

        self.assertEqual(profile_data, expected_data)
'''

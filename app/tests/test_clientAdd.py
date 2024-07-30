'''
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django

django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.db import connection


class ClientAddTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.client.login(username='testuser', password='testpass123')

        # Создаем тестового пользователя, который будет использоваться в POST-запросах
        self.test_user = User.objects.create_user(
            username='clientuser',
            password='clientpass123',
            email='client@example.com'
        )

        # Проверяем и очищаем существующие записи, чтобы избежать конфликтов
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM queue WHERE id_portfolio IS NOT NULL")
            cursor.execute("DELETE FROM requests WHERE id_portfolio IS NOT NULL")
            cursor.execute("DELETE FROM operations_history WHERE id_portfolio IS NOT NULL")
            cursor.execute("DELETE FROM portfolio_to_securitie WHERE id_portfolio IS NOT NULL")
            cursor.execute("DELETE FROM portfolios")
            cursor.execute("DELETE FROM users")
            cursor.execute("DELETE FROM employees")

            cursor.execute("ALTER SEQUENCE employees_id_employee_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE users_id_user_seq RESTART WITH 1")
            cursor.execute("ALTER SEQUENCE portfolios_id_portfolio_seq RESTART WITH 1")

            cursor.execute("INSERT INTO employees (id_employee, id_post) VALUES (1, 1)")
            cursor.execute("INSERT INTO users (id_user, id_employee, id_enterprise) VALUES (1, 1, 1)")
            cursor.execute("INSERT INTO portfolios (id_enterprise, id_employee) VALUES (1, NULL)")
            cursor.execute("INSERT INTO portfolios (id_enterprise, id_employee) VALUES (2, 1)")

            # Вставка данных для проверки функции change_avg_quotation
            cursor.execute(
                "INSERT INTO portfolio_to_securitie (id_portfolio, id_securitie, quantity, quotation) VALUES (1, 1, 10, 100)")
            cursor.execute(
                "INSERT INTO portfolio_to_securitie (id_portfolio, id_securitie, quantity, quotation) VALUES (2, 1, 20, 200)")

    def test_client_add_success(self):
        response = self.client.post('/client_add/', {
            'email': 'client@example.com'
        })
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['message'], 'Клиент добавлен')

    def test_client_add_user_not_exist(self):
        response = self.client.post('/client_add/', {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Такого пользователя не существует')

    def test_client_add_client_not_exist(self):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET id_enterprise=NULL WHERE id_user=1")

        response = self.client.post('/client_add/', {
            'email': 'client@example.com'
        })
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Такого клиента не существует')

    def test_client_add_already_working_with_you(self):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE portfolios SET id_employee=1 WHERE id_enterprise=1")

        response = self.client.post('/client_add/', {
            'email': 'client@example.com'
        })
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Клиент уже работает с вами')

    def test_client_add_already_working_with_other_manager(self):
        response = self.client.post('/client_add/', {
            'email': 'client@example.com'
        })
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Клиент уже работает с другим менеджером')
'''
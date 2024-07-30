import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from app.scripts.funcs import returnJson
from app.views import employeeEdit
import json


class EmployeeEditTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
#ant
    @patch('app.views.connection_db')
    def test_employee_edit_success(self, mock_connection_db):
        # Setup
        request = self.factory.post('/fake-url', {'id': 1, 'email': 'test@example.com', 'name': 'Иванов Иван Иванович'})

        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        # Act
        response = employeeEdit(request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Данные обновлены')

        # проверка вызова execute с sql запросом
        #mock_cursor.execute.assert_any_call(
        #    "update auth_user set email='test@example.com', username='test@example.com' where id=1")
        #mock_cursor.execute.assert_any_call(
        #    "update auth_user set first_name='Иван', last_name='Иванов', patronymic='Иванович' where id=1")

#ant
    @patch('app.views.connection_db')
    def test_employee_edit_validation_error1(self, mock_connection_db):
        request = self.factory.post('/fake-url', {'id': 1, 'email': 'too_long_email_address@example.com', 'name': 'Иванов'})

        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        response = employeeEdit(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)

        self.assertEqual(data['name'], 'ФИО введён некорректно')

    @patch('app.views.connection_db')
    def test_employee_edit_validation_error2(self, mock_connection_db):
        request = self.factory.post('/fake-url', {'id': 1, 'email': 'too_long_email_address', 'name': 'Иванов иван'})

        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        response = employeeEdit(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)

        self.assertEqual(data['email'], 'Введите корректную почту')

#эм ну ок
    @patch('app.views.connection_db')
    def test_employee_edit_validation_error3(self, mock_connection_db):
        request = self.factory.post('/fake-url', {'id': 1, 'email': '', 'name': 'Иванов иван'})

        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        response = employeeEdit(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)

        self.assertEqual(data['email'], 'Введите корректную почту')

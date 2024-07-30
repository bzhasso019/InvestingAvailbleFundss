import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

import unittest
from unittest.mock import patch,MagicMock
from django.test import RequestFactory
from app.scripts.dataProfileEdit.userEdit import clientEdit


class TestClientEdit(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('app.scripts.dataProfileEdit.userEdit.connection_db')
    def test_client_edit_valid_data(self, mock_connection_db):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        mock_cursor.fetchall.return_value = []

        request = self.factory.post('/edit-client/', {
            'email': 'test@example.com',
            'name': 'Иванов Иван',
            'phone': '+71234567890',
            'address': 'ул. Пушкина, д. Колотушкина',
            'type_property': 'Квартира',
            'title': 'ООО Рога и Копыта',
            'id': '1'
        })

        response = clientEdit(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], 'success')

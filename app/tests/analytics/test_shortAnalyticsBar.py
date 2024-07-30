import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from app.scripts.analytics.short.shortAnalyticsBar import shortAnalyticsBar
from django.contrib.auth.models import User
from datetime import datetime

class ShortAnalyticsBarTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = self.create_user()

    def create_user(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass',
            id=1
        )
        return user


    @patch('app.scripts.analytics.short.shortAnalyticsBar.connection_db')
    @patch('app.scripts.analytics.short.shortAnalyticsBar.dt')
    def test_short_analytics_bar(self, mock_dt, mock_connection_db):
        # Setup
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_dt.now.return_value = datetime(2023, 6, 1)

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [(self.user.id,)],
            [(1,)],
            [(datetime(2023, 1, 1), 1000.0),
             (datetime(2023, 2, 1), 1500.0)]
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        month, count, total = shortAnalyticsBar(request)

        self.assertEqual(month, [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май',
            'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
            'Ноябрь', 'Декабрь'
        ])
        self.assertEqual(count, [1000.0, 1500.0] + [0] * 8)
        self.assertEqual(total, 2500.0)


    @patch('app.scripts.analytics.short.shortAnalyticsBar.connection_db')
    def test_short_analytics_bar_no_data(self, mock_connection_db):
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [(self.user.id,)],
            [(1,)],
            []
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        month, count, total = shortAnalyticsBar(request)

        self.assertEqual(month, [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май',
            'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
            'Ноябрь', 'Декабрь'
        ])
        self.assertEqual(count, [0] * 10)
        self.assertEqual(total, 0.0)

        #mock_cursor.close.assert_called()
        #mock_connection.close.assert_called()

    @patch('app.scripts.analytics.short.shortAnalyticsBar.connection_db')
    def test_short_analytics_bar_exception(self, mock_connection_db):
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = Exception("Database error")

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        result, error, _ = shortAnalyticsBar(request)

        self.assertEqual(result, 'Error')
        self.assertEqual(error, '')

        #mock_cursor.close.assert_called()
        #mock_connection.close.assert_called()


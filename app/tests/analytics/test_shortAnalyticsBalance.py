import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

from django.test import TestCase, RequestFactory
from unittest.mock import patch, Mock, MagicMock
from app.scripts.analytics.short import shortAnalyticsBalance
from django.contrib.auth.models import User
class ShortAnalyticsBalanceTests(TestCase):

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

    def test_short_analytics_balance_error(self):
        request = self.factory.get('/')
        request.user = self.create_user()

        result = shortAnalyticsBalance.shortAnalyticsBalance(request)

        self.assertEqual(result, ('Error', ''))

    @patch('app.scripts.analytics.short.shortAnalyticsBalance.connection_db')
    def test_short_analytics_balance_negative_balance(self, mock_connection_db):
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [(self.user.id,)],
            [(1,)],
            [(-100.0, 500.0)]
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        balance, balance_percent = shortAnalyticsBalance.shortAnalyticsBalance(request)

        self.assertEqual(balance, -100.0)
        self.assertEqual(balance_percent, '-120.0')  # Примерный процент для отрицательного баланса

        #mock_cursor.close.assert_called()
        #mock_connection.close.assert_called()

    @patch('app.scripts.analytics.short.shortAnalyticsBalance.connection_db')
    def test_short_analytics_balance_no_portfolio_data(self, mock_connection_db):
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [(self.user.id,)],
            [],
            []
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        balance, balance_percent = shortAnalyticsBalance.shortAnalyticsBalance(request)

        self.assertEqual(balance, 'Error')
        self.assertEqual(balance_percent, '')

        #mock_cursor.close.assert_called()
        #mock_connection.close.assert_called()

    @patch('app.scripts.analytics.short.shortAnalyticsBalance.connection_db')
    def test_short_analytics_balance(self, mock_connection_db):
        # Setup
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [(self.user.id,)],
            [(1,)],
            [(1000.0, 500.0)]
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        balance, balance_percent = shortAnalyticsBalance.shortAnalyticsBalance(request)

        self.assertEqual(balance, 1000.0)
        self.assertEqual(balance_percent, '+100.0')

        #mock_cursor.close.assert_called()
        #mock_connection.close.assert_called()
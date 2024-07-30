import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from app.scripts.analytics.short.shortAnalyticsPie import shortAnalyticsPie
from django.contrib.auth.models import User

class ShortAnalyticsPieTest(TestCase):

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

    @patch('app.scripts.analytics.short.shortAnalyticsPie.connection_db')
    def test_short_analytics_pie(self, mock_connection_db):
        # Setup
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [(self.user.id,)],
            [(1,)],
            [(10, 1.5, 'Акции', 'AAPL'),
             (5, 2.0, 'Акции', 'GOOGL'),
             (8, 1.8, 'Облигации', 'BOND1'),
             (15, 1.2, 'Фонды', 'FUND1'),
             (20, 1.0, 'Валюта и металлы', 'GOLD')]
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection
        graph_pie = shortAnalyticsPie(request)
        #симулируем данные из бд
        expected_graph_pie = [
            {'color': '#634FED', 'count': 25.0, 'name': 'Акции', 'proc': 32.3},
            {'color': '#3AA1FF', 'count': 14.4, 'name': 'Облигации', 'proc': 18.6},
            {'color': '#FF523A', 'count': 18.0, 'name': 'Фонды', 'proc': 23.26},
            {'color': '#F1EDFD', 'count': 20.0, 'name': 'Валюта и металлы', 'proc': 25.84}
        ]

        self.assertEqual(graph_pie, expected_graph_pie)

    #вызываем еррор пустым вызовом
    @patch('app.scripts.analytics.short.shortAnalyticsPie.connection_db')
    def test_short_analytics_pie_error(self, mock_connection_db):
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = Exception('Database error')

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        graph_pie = shortAnalyticsPie(request)

        self.assertEqual(graph_pie, ('Error', ''))



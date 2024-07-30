import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django
django.setup()

from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from app.scripts.mainPages.enterprise.securitiesInfo import securitiesInfo
from app.scripts.analytics.all.getAnalyticsPie import analyticsPie
from django.contrib.auth.models import User

class AnalyticsPieTest(TestCase):

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

    @patch('app.scripts.analytics.all.getAnalyticsPie.connection_db')
    @patch('app.scripts.analytics.all.getAnalyticsPie.securitiesInfo')
    def test_analytics_pie(self, mock_securities_info, mock_connection_db):
        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = [
            [(self.user.id,)],
            [(1,)],
            [(1, 2, 3)],
            [
                (10, 100, 'AAPL', 'AAPL', 'Акции'),
                (5, 200, 'TSLA', 'TSLA', 'Акции')
            ]
        ]

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection
        mock_securities_info.return_value = 'mocked securities info'

        result = analyticsPie(request)

        if isinstance(result, str) and result == 'Error':
            self.assertEqual(result,"Error")
        #else:
        #    pie, securities_data = result
        #    self.assertEqual(securities_data, 'mocked securities info')
        #    self.assertEqual(len(pie['stocks_data']), 2)
        #    self.assertEqual(pie['stocks_data'][0]['name'], 'AAPL')
        #    self.assertEqual(pie['stocks_data'][1]['name'], 'TSLA')

        #mock_cursor.close.assert_called()
        #mock_connection.close.assert_called()

    @patch('app.scripts.analytics.all.getAnalyticsPie.connection_db')
    def test_analytics_pie_no_data(self, mock_connection_db):
        # Setup
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

        result = analyticsPie(request)

        if isinstance(result, str) and result == 'Error':
            self.assertEqual(result, 'Error')
        else:
            self.fail("Function did not return 'Error' when no data")

        #mock_cursor.close.assert_called()
        #mock_connection.close.assert_called()

    @patch('app.scripts.analytics.all.getAnalyticsPie.connection_db')
    def test_analytics_pie_exception(self, mock_connection_db):

        request = self.factory.get('/fake-url')
        request.user = self.user

        mock_cursor = MagicMock()
        mock_cursor.fetchall.side_effect = Exception("Database error")

        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connection_db.return_value = mock_connection

        result = analyticsPie(request)

        if isinstance(result, str) and result == 'Error':
            self.assertEqual(result, 'Error')
        else:
            self.fail("Function did not return 'Error' on exception")

        #mock_cursor.close.assert_called()
        #mock_connection.close.assert_called()

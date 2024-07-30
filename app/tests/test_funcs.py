import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.tests.test_settings')

import django

django.setup()

from django.test import TestCase
from django.http import HttpRequest
from app.scripts.funcs import check, insertSql, getId, checkPass, returnJson, cardValidation
from datetime import datetime as dt


class FuncsTestCase(TestCase):
#ant
    def test_check_email(self):
        valid_email = "test@example.com"
        invalid_email = "invalid-email"

        self.assertFalse(check(valid_email, 'mail'))
        self.assertTrue(check(invalid_email, 'mail'))
#ant
    def test_insertSql(self):
        table = "users"
        params = ["username", "password", "email@example.com"]
        expected_sql = "insert into users\nvalues\n(default, 'username', 'password', 'email@example.com')"

        self.assertEqual(insertSql(table, params), expected_sql)
#ant
    def test_getId(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY)")
            cursor.execute("INSERT INTO test_table DEFAULT VALUES")
            cursor.execute("INSERT INTO test_table DEFAULT VALUES")

            self.assertEqual(getId(cursor, 'test_table', 'id'), 2)

            cursor.execute("DROP TABLE test_table")

    def test_checkPass(self):
        valid_password = "validpass123"
        invalid_password = "invalid pass!"

        self.assertFalse(checkPass(valid_password))
        self.assertTrue(checkPass(invalid_password))

    def test_returnJson(self):
        request = HttpRequest()
        data = {"key": "value"}
        response = returnJson(data=data, status='success', message='message')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(response.content.decode('utf-8'), '{"key": "value"}')

    def test_cardValidation(self):
        valid_amount = 100
        invalid_amount = -100
        valid_card_number = "1234567812345678"
        invalid_card_number = "1234"
        valid_card_date = [6, 25]
        invalid_card_date = [13, 25]  # месяц инвалид

        errors = cardValidation(valid_amount, valid_card_number, valid_card_date)
        self.assertEqual(errors, {})

        errors = cardValidation(invalid_amount, valid_card_number, valid_card_date)
        self.assertIn('amount', errors)

        errors = cardValidation(valid_amount, invalid_card_number, valid_card_date)
        self.assertIn('card_number', errors)

        errors = cardValidation(valid_amount, valid_card_number, invalid_card_date)
        self.assertIn('card_date', errors)

        invalid_card_date_past = [6, 20]
        errors = cardValidation(valid_amount, valid_card_number, invalid_card_date_past)
        self.assertIn('card_date', errors)

import unittest

from django.test import Client
from django.urls import reverse
from rest_framework import status

client = Client()


class VerifyTestCases(unittest.TestCase):
    def setUp(self):
        self.valid_payload = {
            'third_party_company_name': 'UD Saragih Tbk'
        }

        self.valid_payload_f = {
            'third_party_company_name': 'PT Hutasoit Januar (Persero) Tbk'
        }

        self.not_found_payload = {
            'third_party_company_name': 'FAANG'
        }

        self.invalid = {
            'third_party_company_name': ''
        }

    def test_check_valid_true(self):
        response = client.post(reverse('verify_company'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'vendor_company': {'UD Saragih Tbk'}, 'user': {True}})

    def test_check_valid_false(self):
        response = client.post(reverse('verify_company'), self.valid_payload_f)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'vendor_company': {'PT Hutasoit Januar (Persero) Tbk'}, 'user': {False}})

    def test_check_notfound(self):
        response = client.post(reverse('verify_company'), self.not_found_payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "FAANG Vendor Does Not Exist!")

    def test_check_invalid(self):
        response = client.post(reverse('verify_company'), self.invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Vendor Name is required!")


class TransactionTestCases(unittest.TestCase):
    def setUp(self):
        self.valid_payload = {
            'company_name': 'Perum Prasetya Permadi',
            'company_vendor': 'PT Putra',
            'from_date': '2020-04-05 08:42:35',
            'to_date': '2020-05-06 14:03:08'
        }
        self.not_found_payload = {
            'company_name': 'Perum Prasetya Permadi',
            'company_vendor': 'FAANG',
            'from_date': '2020-04-05 08:42:35',
            'to_date': '2020-05-06 14:03:08'
        }

        self.invalid = {
            'company_name': '',
            'company_vendor': '',
            'from_date': '',
            'to_date': ''
        }

        self.greater_date = {
            'company_name': 'Perum Prasetya Permadi',
            'company_vendor': 'PT Putra',
            'from_date': '2020-06-05 08:42:35',
            'to_date': '2020-05-06 14:03:08'
        }

        self.invalid_date = {
            'company_name': 'Perum Prasetya Permadi',
            'company_vendor': 'PT Putra',
            'from_date': '-06-05 08:42:35',
            'to_date': '2020-05-06 14:03:08'
        }

    def test_check_valid(self):
        response = client.post(reverse('transaction_frequency'), self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"companies": "Perum Prasetya Permadi & PT Putra", "transactions": {47}})

    def test_check_notfound(self):
        response = client.post(reverse('transaction_frequency'), self.not_found_payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "FAANG Vendor Does Not Exist!")

    def test_check_invalid(self):
        response = client.post(reverse('transaction_frequency'), self.invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Vendor Name is required!")

    def test_check_greater_date(self):
        response = client.post(reverse('transaction_frequency'), self.greater_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "to_date, to_date must be bigger than from_date")

    def test_check_invalid_date(self):
        response = client.post(reverse('transaction_frequency'), self.invalid_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Date: invalid_format")

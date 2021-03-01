import unittest
import os
from libs.payment_handler import PaymentAnalyzer
from libs.csv_handler import CSVHandler


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.analyzer = PaymentAnalyzer()

    def tearDown(self):
        os.remove('results/tests/agent_collection_report.csv')
        os.remove('results/tests/days_from_suspension_report.csv')
        os.remove('results/tests/payment_type_report.csv')
        os.rmdir('results/tests')

    def test_file_created(self):
        input_data = CSVHandler.read('inputs/payments_test.csv')
        self.analyzer.handle(input_data, 'tests')
        directory = os.path.dirname('results/tests/agent_collection_report.csv')
        self.assertTrue(os.path.exists(directory))

    def test_days_from_suspension(self):
        input_data = CSVHandler.read('inputs/payments_test.csv')
        self.analyzer.handle(input_data, 'tests')

        correct_data = [
            {'device_id': '8512', 'days_from_suspension': '37'},
            {'device_id': '8511', 'days_from_suspension': '36'},
            {'device_id': '8510', 'days_from_suspension': '0'},
        ]

        output_data = CSVHandler.read('results/tests/days_from_suspension_report.csv')
        self.assertEqual(correct_data, output_data)

    def test_payment_type_report(self):
        input_data = CSVHandler.read('inputs/payments_test.csv')
        self.analyzer.handle(input_data, 'tests')

        correct_data = [
            {'payment_type': 'BANK_DEPOSIT', 'total_amount': '0'},
            {'payment_type': 'CASH', 'total_amount': '120'},
            {'payment_type': 'REFFERAL', 'total_amount': '60'},
        ]

        output_data = CSVHandler.read('results/tests/payment_type_report.csv')
        self.assertEqual(correct_data, output_data)

    def test_agent_collection_report(self):
        input_data = CSVHandler.read('inputs/payments_test.csv')
        self.analyzer.handle(input_data, 'tests')

        correct_data = [
            {'agent_user_id': '17', 'date': '2021-01-07', 'payment_type': 'REFFERAL', 'total_amount': '60'},
            {'agent_user_id': '17', 'date': '2021-01-08', 'payment_type': 'CASH', 'total_amount': '120'},
        ]

        output_data = CSVHandler.read('results/tests/agent_collection_report.csv')
        self.assertEqual(correct_data, output_data)

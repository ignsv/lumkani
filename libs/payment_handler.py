import datetime

from libs.csv_handler import CSVHandler
from libs.utils import fake_now


class PaymentAnalyzer:

    def handle_days_from_suspension(self, data):
        device_id_set = set(item['device_id'] for item in data)
        result_list = []
        for device_id in device_id_set:
            latest_successful_date = datetime.datetime.min
            while True:
                payment = next((item for item in data if item['device_id'] == device_id), None)
                if payment is not None:
                    data.remove(payment)
                else:
                    break
                payment_date = datetime.datetime.strptime(payment['created'], '%Y-%m-%d %H:%M:%S')
                if payment_date > latest_successful_date and payment['status'] == 'SUCCESSFUL':
                    latest_successful_date = payment_date
            #  TODO CHANGE to datetime.datetime.now()
            days_from_suspension = 0
            if latest_successful_date + datetime.timedelta(days=90) > fake_now():
                delta = (latest_successful_date + datetime.timedelta(days=90)) - fake_now()
                days_from_suspension = delta.days
            result_list.append({'device_id': device_id, 'days_from_suspension': days_from_suspension})

        return result_list

    def handle(self, data, result_directory):
        days_from_suspension_result = self.handle_days_from_suspension(data)
        CSVHandler.write('days_from_suspension_report.csv', f'results/{result_directory}',
                         days_from_suspension_result)

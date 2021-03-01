import datetime
import collections

from libs.csv_handler import CSVHandler
from libs.utils import fake_now


class PaymentAnalyzer:

    def handle_days_from_suspension(self, input_data):
        data = input_data.copy()
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

        return sorted(result_list, key=lambda k: k['days_from_suspension'], reverse=True)

    def handle_agent_collection(self, input_data):
        data = input_data.copy()
        agent_user_id_list = sorted(list(set(item['agent_user_id'] for item in data)))
        result_list = []
        for agent_user_id in agent_user_id_list:
            payment_type_date_amount_list = []
            payment_date_set = set()
            while True:
                payment = next((item for item in data if item['agent_user_id'] == agent_user_id), None)
                if payment is not None:
                    data.remove(payment)
                else:
                    break
                sorted(list(payment_date_set.add(str(datetime.datetime.strptime(payment['created'], '%Y-%m-%d %H:%M:%S').date()))))
                payment_type_date_amount_list.append(
                    {
                        'payment_type': payment['payment_type'],
                        'payment_amount': payment['payment_amount'],
                        'date': str(datetime.datetime.strptime(payment['created'], '%Y-%m-%d %H:%M:%S').date()),
                        'status': payment['status']
                    }
                )

            for payment_date in payment_date_set:
                date_amount_dict = dict()
                for item in payment_type_date_amount_list:
                    if item['date'] == payment_date and item['status'] == 'SUCCESSFUL':
                        if item['date'] not in date_amount_dict:
                            date_amount_dict[item['date']] = int(item['payment_amount'])
                        else:
                            date_amount_dict[item['date']] += int(item['payment_amount'])

                ordered_amount_by_date = collections.OrderedDict(sorted(date_amount_dict.items()))
                for key, value in ordered_amount_by_date.items():
                    result_list.append({
                        'agent_user_id': agent_user_id,
                        'date': key,
                        'payment_type': payment_type,
                        'total_amount': value
                    })
        return result_list

    def handle(self, data, result_directory):
        days_from_suspension_result = self.handle_days_from_suspension(data)
        CSVHandler.write('days_from_suspension_report.csv', f'results/{result_directory}',
                         days_from_suspension_result)

        agent_collection_result = self.handle_agent_collection(data)
        CSVHandler.write('agent_collection_report.csv', f'results/{result_directory}',
                         agent_collection_result)

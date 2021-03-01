import sys

from libs.payment_handler import PaymentAnalyzer
from libs.csv_handler import CSVHandler

# TODO RETURN
# if len(sys.argv) != 3:
#     raise Exception('There must be only 2 arguments in script')

payment_analyzer = PaymentAnalyzer()
#  TODO change to sys.argv[1]
input_data = CSVHandler.read('payments.csv')
#  TODO change to sys.argv[2]
payment_analyzer.handle(input_data, result_directory='common')



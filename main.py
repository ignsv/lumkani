import sys

from libs.payment_handler import PaymentAnalyzer
from libs.csv_handler import CSVHandler

if len(sys.argv) != 3:
    raise Exception('There must be only 2 arguments in script')

payment_analyzer = PaymentAnalyzer()
input_data = CSVHandler.read('inputs/' + sys.argv[1])
payment_analyzer.handle(input_data, sys.argv[2])



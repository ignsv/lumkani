import csv
import os


class CSVHandler:

    @classmethod
    def write(cls, filename, directory, data):
        directory = os.path.dirname(f'{directory}/{data}')
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open('{}/{}'.format(directory, filename), 'w+', newline='') as csvfile:
            if data:
                fieldnames = [key for key in data[0]]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    writer.writerow(item)
    @classmethod
    def read(cls, filepath):
        input_data = []
        with open('inputs/{}'.format(filepath), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                input_data.append(row)

        return input_data

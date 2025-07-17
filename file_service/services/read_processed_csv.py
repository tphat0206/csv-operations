import csv
import logging

logger = logging.getLogger(__name__)

class ReadProcessedCsv:
    MAX_INT = 999999
    def __init__(self, file_path, n_value):
        self.file_path = file_path
        self.n_value = n_value

    def exec(self):
        data = []
        if self.n_value is None:
            self.n_value = self.MAX_INT
        try:
            with open(self.file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if self.n_value > 0:
                        data.append(row)
                        self.n_value -= 1
            return data
        except FileNotFoundError:
            logger.error(f'The file {self.file_path} was not found.')
            return None
        except Exception as e:
            logger.error(f'An error occurred: {e}')
            return None
import json

import pandas as pd


class DeduplicatedCsvExec:
    def __init__(self, file_path, parameters):
        self.file_path = file_path
        self.parameters = json.loads(parameters)

    def exec(self):
        df = pd.read_csv(self.file_path)
        return df.drop_duplicates()
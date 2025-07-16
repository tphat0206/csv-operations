import json

import pandas as pd


class UniqueCsvExec:
    def __init__(self, file_path, parameters):
        self.file_path = file_path
        self.column_name = json.loads(parameters).get('column_name', '')

    def exec(self):
        df = pd.read_csv(self.file_path)
        return pd.DataFrame(df[self.column_name].unique(), columns=[self.column_name])
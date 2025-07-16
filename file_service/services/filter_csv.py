import json

import pandas as pd


class FilterCsvExec:
    def __init__(self, file_path, parameters):
        self.file_path = file_path
        self.filter_params = json.loads(parameters)

    def exec(self):
        df = pd.read_csv(self.file_path)
        for condition in self.filter_params:
            column_name = condition.get('column', '')
            value = condition.get('value', '')
            if column_name not in df.columns:
                raise ValueError(f"Filter column '{column_name}' not found in the CSV file.")
            df = df[df[column_name].astype(str) == str(value)]

        return df

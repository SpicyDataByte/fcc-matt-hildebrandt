import pandas as pd

class ColumnValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df['failed_columns'] = [[] for _ in range(len(df))]

    def validate(self, column: str, test_func):
        valid_mask = self.df[column].apply(test_func)
        self.df.loc[~valid_mask, 'failed_columns'] = self.df.loc[~valid_mask, 'failed_columns'].apply(
            lambda current: current + [column]
        )

    def get_invalid_rows(self):
        return self.df[self.df['failed_columns'].apply(len) > 0].copy()

def is_clean_name(name):
    if pd.isna(name) or str(name).strip() == '':
        return False
    name_str = str(name)
    return all(c not in name_str for c in ['@']) and len(name_str.split()) == 1

def is_not_empty(value):
    if isinstance(value, str):
        return value.strip() != ''
    return pd.notnull(value)

import pandas as pd

def extract_data(file_path):
    print(f"Loading data from {file_path}")
    return pd.read_csv(file_path)

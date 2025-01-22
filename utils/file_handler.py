import pandas as pd

def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return None

def add_record(file_path, record):
    df = pd.DataFrame([record])
    try:
        existing_data = pd.read_csv(file_path)
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(file_path, index=False)

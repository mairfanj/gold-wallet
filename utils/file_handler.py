import pandas as pd
import os

def load_data(file_path):
    """
    Load data from a CSV file.
    Returns an empty DataFrame if the file does not exist.
    """
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error
    else:
        return pd.DataFrame()  # Return empty DataFrame if file does not exist

def save_data(file_path, data):
    """
    Save a DataFrame to a CSV file.
    Overwrites the file if it already exists.
    """
    try:
        data.to_csv(file_path, index=False)
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")

def add_record(file_path, record):
    """
    Add a new record to the specified CSV file.
    Creates the file if it does not exist.
    """
    new_data = pd.DataFrame([record])
    try:
        if os.path.exists(file_path):
            existing_data = pd.read_csv(file_path)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data
        updated_data.to_csv(file_path, index=False)
    except Exception as e:
        print(f"Error adding record to {file_path}: {e}")

def ensure_column_exists(file_path, column_name, default_value=None):
    """
    Ensure a specific column exists in the CSV file.
    Adds the column with a default value if it's missing.
    """
    data = load_data(file_path)
    if column_name not in data.columns:
        data[column_name] = default_value
        save_data(file_path, data)

def ensure_file_exists(file_path, default_columns):
    """
    Ensure the specified file exists with the provided default columns.
    Creates the file with default columns if it doesn't exist.
    """
    if not os.path.exists(file_path):
        pd.DataFrame(columns=default_columns).to_csv(file_path, index=False)

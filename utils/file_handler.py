import pandas as pd

def load_data(file_path):
    """Load jewelry records from a CSV file."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Date", "Transaction Type", "Price (RM)", "Weight (grams)", "Type", "Shop Name", "Notes"])

def save_data(file_path, data):
    """Save the updated DataFrame to a CSV file."""
    data.to_csv(file_path, index=False)

def add_record(file_path, record):
    """Add a new record to the CSV file."""
    df = pd.DataFrame([record])
    try:
        existing_data = pd.read_csv(file_path)
        df = pd.concat([existing_data, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(file_path, index=False)

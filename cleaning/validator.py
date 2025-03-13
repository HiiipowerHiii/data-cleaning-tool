import pandas as pd
import os

def is_valid_file_format(file_path):
    valid_formats = ['.csv', '.xlsx']
    file_extension = os.path.splitext(file_path)[1]
    return file_extension in valid_formats

def read_file(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        return None

def identify_invalid_rows(data):
    invalid_rows = []
    for index, row in data.iterrows():
        if row.isnull().any(): 
            invalid_rows.append(index)
    return invalid_rows

def validate_data_file(file_path):
    if not is_valid_file_format(file_path):
        print(f"Error: Unsupported file format. Supported formats are CSV and Excel.")
        return

    try:
        data = read_file(file_path)
        if data is None:
            print("Error: Couldn't read the file. The file may be corrupted or unsupported format.")
            return

        invalid_rows = identify_invalid_rows(data)
        if invalid_rows:
            print(f"Invalid rows identified: {invalid_rows}")
        else:
            print("No invalid data found.")
    except Exception as e:
        print(f"Error occurred while processing file: {e}")

from dotenv import load_dotenv
load_dotenv()

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH')
validate_data_file(DATA_FILE_PATH)
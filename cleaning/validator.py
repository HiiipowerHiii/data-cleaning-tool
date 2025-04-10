import pandas as pd
import os
from dotenv import load_dotenv

def is_valid_file_format(file_path):
    try:
        valid_formats = ['.csv', '.xlsx']
        file_extension = os.path.splitext(file_path)[1]
        return file_extension in valid_formats
    except Exception as e:
        print(f"Error determining file format: {e}")
        return False

def read_file(file_path):
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)
    except FileNotFoundError:
        print("Error: File not found.")
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
    except Exception as e:
        print(f"General error occurred while reading file: {e}")
    return None

def identify_invalid_rows(data):
    try:
        invalid_rows = []
        for index, row in data.iterrows():
            if row.isnull().any():
                invalid_rows.append(index)
        return invalid_rows
    except Exception as e:
        print(f"Error identifying invalid rows: {e}")
        return []

def validate_data_file(file_path):
    if not file_path or not is_valid_file_format(file_path):
        print(f"Error: Unsupported or missing file format. Supported formats are CSV and Excel.")
        return
    
    data = read_file(file_path)
    if data is None:
        print("Error: Couldn't process the file. The file may be corrupted, unsupported format, or not found.")
        return
    
    try:
        invalid_rows = identify_invalid_rows(data)
        if invalid_rows:
            print(f"Invalid rows identified: {invalid_rows}")
        else:
            print("No invalid data found.")
    except Exception as e:
        print(f"Error occurred while validating data: {e}")

load_dotenv()

DATA_FILE_PATH = os.getenv('DATA_FILE_PATH')

validate_data_file(DATA_FILE_PATH)
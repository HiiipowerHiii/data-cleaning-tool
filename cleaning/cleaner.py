import pandas as pd
import numpy as np
from datetime import datetime

def remove_empty_rows_and_columns(df):
    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    return df

def handle_missing_values(df, strategy='mean', default_value=None, columns=None):
    if columns is None:
        columns = df.columns
    
    for col in columns:
        if df[col].isnull().any():
            if strategy == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
            elif strategy == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            elif strategy == 'default':
                if default_value is not None:
                    df[col].fillna(default_value, inplace=True)
                else:
                    raise ValueError("Default value must be provided for 'default' strategy.")
            else:
                raise ValueError("Strategy not recognized. Use 'mean', 'median', or 'default'.")

    return df

def remove_duplicate_rows(df):
    df.drop_duplicates(inplace=True)
    return df

def normalize_data_format(df, date_columns=None, numeric_columns=None):
    if date_columns is not None:
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    if numeric_columns is not None:
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df
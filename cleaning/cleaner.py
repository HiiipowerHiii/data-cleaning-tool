import pandas as pd
import numpy as np
from datetime import datetime

def remove_empty_rows_and_columns(df):
    return df.dropna(axis=0, how='all').dropna(axis=1, how='all')

def handle_missing_values(df, strategy='mean', default_value=None, columns=None):
    if columns is None:
        columns = df.columns

    strategies = {
        'mean': lambda col: df[col].mean(),
        'median': lambda col: df[col].median(),
        'default': lambda col: default_value if default_value is not None else ValueError("Default value must be provided for 'default' strategy.")
    }

    for col in columns:
        if df[col].isnull().any():
            df[col].fillna(strategies[strategy](col), inplace=True) if strategy in strategies else ValueError("Strategy not recognized. Use 'mean', 'median', or 'default'.")

    return df

def remove_duplicate_rows(df):
    return df.drop_duplicates()

def normalize_data_format(df, date_columns=None, numeric_columns=None):
    if date_columns is not None:
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    if numeric_columns is not None:
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    return df
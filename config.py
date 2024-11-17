import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
CLEANED_DATA_DIR = os.path.join(DATA_DIR, 'cleaned')

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
MAX_FILE_SIZE_MB = 10  # Maximum file size in MB

DEFAULT_FILL_METHOD = 'mean'  # Options: 'mean', 'median', 'zero'
REMOVE_DUPLICATES = True
NORMALIZE_DATES = True
NORMALIZE_NUMERIC_FORMATS = True

API_HOST = '127.0.0.1'
API_PORT = 5000

os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(CLEANED_DATA_DIR, exist_ok=True)

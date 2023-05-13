from sys import platform
from tools.operation_system import OperationSystem

IGNORE = [
    'venv',
    'Khorn_data.txt',
    '.idea'
]

if platform == OperationSystem.LINUX:
    SEPARATOR_DIR = '/'
else:
    SEPARATOR_DIR = '\\'

DATABASE_NAME = 'data/Khorn_data.db'
PATH_TO_DATA_TXT = 'Khorn_data.txt'

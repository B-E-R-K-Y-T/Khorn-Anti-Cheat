from sys import platform
from tools.operation_system import OperationSystem

IGNORE = [
    'venv',
    'khorn_targets.txt',
    '.idea',
    'khornignore.db',
    '.gitignore',
    '.git',
]

INVERT_IGNORE = False

if platform == OperationSystem.WINDOWS_32 or platform == OperationSystem.WINDOWS_64:
    SEPARATOR_DIR = '\\'
    DATABASE_NAME = 'data\\khornignore.db'
else:
    SEPARATOR_DIR = '/'
    DATABASE_NAME = 'data/khornignore.db'   

PATH_TO_DATA_TXT = 'khorn_targets.txt'

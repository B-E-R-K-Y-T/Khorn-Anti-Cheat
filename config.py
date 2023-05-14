from sys import platform
from tools.operation_system import OperationSystem

IGNORE = [
    'venv',
    'khorn_targets.txt',
    '.idea',
    'khornignore.db',
    '.git',
]

INVERT_IGNORE = False

if platform == OperationSystem.LINUX:
    SEPARATOR_DIR = '/'
else:
    SEPARATOR_DIR = '\\'

DATABASE_NAME = 'data/khornignore.db'
PATH_TO_DATA_TXT = 'khorn_targets.txt'

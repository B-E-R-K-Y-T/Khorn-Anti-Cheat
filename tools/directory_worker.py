import os
import tools.crypt as crypt

from sys import platform
from codecs import open
from tools.parser import ParserCryptFile, replace_dict, remove_space
from tools.exceptions import InvalidDir
from config import SEPARATOR_DIR, PATH_TO_DATA_TXT, INVERT_IGNORE, BEGIN_OPERATOR
from tools.operation_system import OperationSystem
from tools.database_worker import Database
from tools.speed_test import trace_speed

DATABASE = Database()


def _is_ignore(root: str):
    for ignore_path in DATABASE.get_ignore_items():
        for sub_root in root.split(SEPARATOR_DIR):
            if INVERT_IGNORE:
                if sub_root == ignore_path or sub_root.startswith('trace_speed'):
                    return False 
            else:
                if sub_root == ignore_path or sub_root.startswith('trace_speed'):
                    return True 

    return True if INVERT_IGNORE else False


def _get_convert_str_to_path_list(path):
    path.pop(-1)
    path = [line for line in path if line]
    res = ''.join([SEPARATOR_DIR + line for line in path])

    return res


def _split_path_for_os(path):
    if platform == OperationSystem.WINDOWS_32 or platform == OperationSystem.WINDOWS_64:
        return path.split('\\')
    else:
        return path.split('/')


def _format_path_to_os(path):
    if platform == OperationSystem.WINDOWS_32 or platform == OperationSystem.WINDOWS_64:
        return path[1:]
    else:
        return path


def get_my_directory(path=__file__):
    return _format_path_to_os(_get_convert_str_to_path_list(_split_path_for_os(path)))


@trace_speed
def _crypt_directory(directory):
    res = {}

    c = crypt.Crypt()

    for name_file, file in directory.get_files():
        if _is_ignore(name_file):
            continue

        print(f'<KHORN> SET TARGET TO FILE: {name_file}')

        res[name_file] = ''

        try:
            for line in file:
                line = replace_dict({'\n': '', '\t': ''}, line)

                if line.isspace():
                    continue

                res[name_file] += c.crypt_mode(line)
        except UnicodeDecodeError as _:
            pass

    return res


class DirectoryReader:
    def __init__(self, path_directory=get_my_directory()):
        self.path_directory = path_directory

    def get_directory_as_dict(self):
        directory = {}

        for root, _, files in os.walk(self.path_directory):
            if files and not _is_ignore(root):
                directory[root] = files

        return directory

    def get_files(self):
        for path, files in self.get_directory_as_dict().items():
            for file in files:
                name_file = f'{path}{SEPARATOR_DIR}{file}'
                with open(name_file, mode='r', encoding='utf-8') as target_file:
                    yield name_file, target_file


class DirectorySaver:
    def __init__(self, path_directory=get_my_directory()):
        self.directory = DirectoryReader(path_directory)

    def save_directory(self, save_mode):
        save_mode(_crypt_directory(self.directory))


class FileSaver:
    def __init__(self):
        ...

    def __call__(self, directory: dict):
        with open(PATH_TO_DATA_TXT, mode='w', encoding='utf=8') as file:
            for name, text_file in directory.items():
                if not _is_ignore(name):
                    file.write(f'{name=}=[{text_file}];')


class DirectoryInspector:
    def __init__(self, path_directory=get_my_directory(), path_data=PATH_TO_DATA_TXT):
        self.directory = DirectoryReader(path_directory)
        try:
            self.parser = ParserCryptFile(path_data)
        except FileNotFoundError as _:
            raise FileNotFoundError(f'<KHORN> FILE {path_data} NOT FOUND! YOU BANNED!')
        self.crypt = crypt.Crypt()

    @trace_speed
    def check_valid_file(self):
        origin_directory = self.parser.get_crypt_directory()

        for name_file, target_file in self.directory.get_files():
            if _is_ignore(name_file):
                continue

            print(f'<KHORN> CHECK FILE: {name_file}...')

            try:
                old = self.crypt.decrypt_mode(origin_directory.get(name_file))
                new = remove_space(replace_dict({'\n': '', '\t': ''}, target_file.read()))

                if not (old and new):
                    continue

                if old != new:
                    raise InvalidDir(f'<KHORN> YOUR DIRECTORY INVALID! FILE: {name_file}')
                else:
                    print(f'<KHORN> IT\'S OK!')
            except UnicodeDecodeError as _:
                continue


__all__ = (
    DirectoryInspector.__name__,
    FileSaver.__name__,
    DirectorySaver.__name__,
    DirectoryReader.__name__,
    get_my_directory.__name__,
)

if __name__ == '__main__':
    # d = DirectoryReader(path_directory='/home/berkyt/PycharmProjects/Khorn')
    # print(d.get_directory_as_dict())
    # for _, i in d.get_files():
    #     for j in i:
    #         print(j)

    DirectorySaver(path_directory='/home/berkyt/PycharmProjects/Khorn/~test').save_directory(FileSaver())

    print(get_my_directory())

import os
import tools.crypt as crypt

from sys import platform
from codecs import open
from tools.parser import ParserCryptFile, replace_dict, remove_space
from tools.exceptions import InvalidDir
from config import SEPARATOR_DIR, PATH_TO_DATA_TXT, IGNORE
from tools.operation_system import OperationSystem
from tools.database_worker import Database

DATABASE = Database()


def is_ignore(root: str):
    for ignore_path in DATABASE.get_ignore_items():
        for sub_root in root.split(SEPARATOR_DIR):
            # print(sub_root, ignore_path)
            if sub_root == ignore_path:
                return True

    return False


def get_my_directory(path=__file__):
    os_name = platform

    if os_name == OperationSystem.LINUX:
        path = path.split('/')
    else:
        path = path.split('\\')

    path.pop(-1)
    path = [line for line in path if line]
    res = ''.join([SEPARATOR_DIR + line for line in path])

    if os_name == OperationSystem.LINUX:
        return res
    else:
        return res[1:]


class DirectoryReader:
    def __init__(self, path_directory=get_my_directory()):
        self.path_directory = path_directory

    def get_directory_as_dict(self):
        directory = {}

        for root, _, files in os.walk(self.path_directory):
            if files and not is_ignore(root):
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
        save_mode(crypt_directory(self.directory))


class FileSaver:
    def __init__(self):
        ...

    def __call__(self, directory: dict):
        with open(PATH_TO_DATA_TXT, mode='w', encoding='utf=8') as file:
            for name, text_file in directory.items():
                if not is_ignore(name):
                    file.write(f'{name=}=[{text_file}];')


class DirectoryInspector:
    def __init__(self, path_directory=get_my_directory(), path_data=PATH_TO_DATA_TXT):
        self.directory = DirectoryReader(path_directory)
        try:
            self.parser = ParserCryptFile(path_data)
        except FileNotFoundError as _:
            raise FileNotFoundError(f'<KHORN> FILE {path_data} NOT FOUND! YOU BANNED!')
        self.crypt = crypt.Crypt()

    def check_valid_file(self):
        origin_directory = self.parser.get_crypt_directory()

        for name_file, target_file in self.directory.get_files():
            print(f'<KHORN> CHECK FILE: {name_file}...')

            if is_ignore(name_file):
                continue

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


def crypt_directory(directory: DirectoryReader):
    res = {}

    c = crypt.Crypt()

    for name_file, file in directory.get_files():
        print(name_file, file)
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


if __name__ == '__main__':
    # d = DirectoryReader(path_directory='/home/berkyt/PycharmProjects/Khorn')
    # print(d.get_directory_as_dict())
    # for _, i in d.get_files():
    #     for j in i:
    #         print(j)

    DirectorySaver(path_directory='/home/berkyt/PycharmProjects/Khorn/~test').save_directory(FileSaver())

    print(get_my_directory())

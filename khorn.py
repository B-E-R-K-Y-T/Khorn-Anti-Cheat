from tools.directory_worker import *


def listen():
    DirectorySaver(get_my_directory(__file__)).save_directory(FileSaver())

    while True:
        d_l = DirectoryInspector(get_my_directory(__file__))
        d_l.check_valid_file()


if __name__ == '__main__':
    listen()
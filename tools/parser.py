from codecs import open


class ParserCryptFile:
    def __init__(self, path: str):
        self.directory = self.convert_directory_to_dict(open(path, mode='r', encoding='utf=8'))

    def convert_directory_to_dict(self, file):
        text = file.read().split(';')
        res = {}

        for item in text:
            if item:
                name, value = self.__get_name(item), self.__get_value(item)
                name = replace_dict({'\\\\': '\\'}, name)
                res[name] = value

        return res

    def get_crypt_directory(self):
        return self.directory

    @staticmethod
    def __get_name(item):
        return item.split('\'=')[0][6:]

    @staticmethod
    def __get_value(item):
        return item.split('\'=')[1][1:-1]


def replace_dict(dict_words: dict, line: str) -> str:
    for old_word, new_word in dict_words.items():
        line = line.replace(str(old_word), str(new_word))

    return line


def remove_space(string):
    res = ''

    for line in string:
        if line.isspace():
            continue
        else:
            res += line

    return res


if __name__ == '__main__':
    p = ParserCryptFile(path='/home/berkyt/PycharmProjects/Khorn/tools/Khorn_data.txt')
    print(p.get_crypt_directory())

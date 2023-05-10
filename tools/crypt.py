import random


class Crypt:
    def __init__(self):
        self.abc = r' iSК%?вnЩфНW7}ЖЕsВзgоу,Ьм.T-ЁdRD]Ц(ILUнТ3ркИc*ч=ЫйwP;{СJ\/цCъe0vЯ#Q[' \
                   r'Л"YЧ\'еЗPaZпKД86mГ1FЮqyЪBOт<УЙ@$ОащШг!ПVfubРlжzшX4БM9kсьG5бtxHМ_Аядэr&:иopФE)Э^ANл+j>ю`Ххыё2h|~ ' \
                   r'😀😃😄😁😆🥹😊☺️🥲🤣😂😅😇🙂🙃😉😌😍😋😚😙😗😘🥰😛😝😜🤪🤨🧐😏🥳🤩🥸😎🤓😒😞😔😟😕🙁🥺😩😫😖' \
                   r'😣☹️😢😭😤😠😡🤬😱😶‍🌫️🥶🥵😳🤯😨😰😥😓🤗🤔🫠🤫🫡🫢🤭🫣🤥😶🫥😐🫤😑😮😧😦😯🙄😬😲🥱😴🤤😪😮‍💨🤮🤢' \
                   r'🥴🤐😵‍💫😵🤧😷🤒🤕🤑🤠💩🤡👺👹👿😈👻💀☠️👽👾🤖🎃😺😸😹😻😼🤲🏻🫶🏻😾😿🙀😽👐🏻🙌🏻👏🏼🤝👍🏻💪🏻🦾' \
                   r'💋👄👄🫦🦷👅👤🫂👶🏼👶🏾🫀👶🏾👶🏻'
        self.crypt_offset = self.generate_crypt_offset()
        self.max_key = max(list(map(int, self.get_decrypt_dict(self.crypt_offset).keys())))

    @staticmethod
    def generate_crypt_offset():
        return random.randint(100, 450)

    def get_crypt_dict(self, crypt_offset):
        crypt_dict = {}

        for offset, item in enumerate(self.abc):
            crypt_dict[item] = str(offset + crypt_offset)

        return crypt_dict

    def get_decrypt_dict(self, crypt_offset):
        decrypt_dict = {}

        for offset, item in enumerate(self.abc):
            decrypt_dict[str(offset + crypt_offset)] = item

        return decrypt_dict

    def get_separate_code(self):
        return str(random.randint(self.max_key + 201, self.max_key + 250))

    @staticmethod
    def get_text_trash():
        res = ''
        abc = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for _ in range(random.randint(0, 4)):
            res += random.choice(list(abc))

        return res.replace(' ', '')

    def get_trash(self):
        return ''.join(
            [self.get_text_trash() +
             str(random.randint(self.max_key + 1, self.max_key + 200)) +
             self.get_text_trash()  # + self.get_separate_code()
             for _ in range(random.randint(0, 1))
             if random.randint(0, 1)]
        )

    def cryptf_mode(self):
        text = ''

        file = input('cryptf >>> ')
        try:
            with open(file, mode='r', encoding='utf-8') as f:
                for i in f:
                    text += i

            crypt_text = self.crypt_mode(text)

            print(crypt_text, file=open(file + '.crypt', 'w', encoding='utf-8'))
        except FileNotFoundError as _:
            print('---> File not found!')
            return

    def crypt_mode(self, line: str, mode='crypt_call'):
        text = ''

        if mode == 'crypt':
            text = input('crypt >>> ')
        elif mode == 'cryptf':
            file = input('cryptf >>> ')
            try:
                with open(file, mode='r', encoding='utf-8') as f:
                    for i in f:
                        text += i
            except FileNotFoundError as _:
                print('---> File not found!')
                return
        elif mode == 'crypt_call':
            text = line

        crypt_text = ''
        crypt_dict = self.get_crypt_dict(self.crypt_offset)

        for crypt_s in text:
            if crypt_s in crypt_dict.keys():
                crypt_text += self.get_trash() + \
                              crypt_dict[crypt_s] + \
                              self.get_separate_code() + \
                              self.get_trash()

        crypt_text += str(self.crypt_offset) + self.get_text_trash()

        if mode == 'crypt':
            return crypt_text
        elif mode == 'crypt_call':
            return crypt_text
        elif mode == 'cryptf':
            print(crypt_text, file=open(file + '.crypt', 'w', encoding='utf-8'))

    def get_real_symbols(self, text, crypt_offset):
        res = ''

        for symbol in text:
            res += symbol

            if not res.isdigit():
                res = ''

            if len(res) == 3:
                if res in self.get_decrypt_dict(crypt_offset).keys():
                    yield res

                res = ''

    @staticmethod
    def get_crypt_offset(text):
        res = ''

        for symbol in reversed(text):
            if symbol.isdigit():
                res += symbol
            if len(res) == 3:
                break
            elif len(res) > 3:
                raise Exception('Offset not found.')

        try:
            res = res[-1] + res[1] + res[0]
            return int(res)
        except IndexError as _:
            print('---> Empty data!')
            return
        except ValueError as _:
            print('---> Empty data!')
            return

    def decrypt_mode(self, line, mode='decrypt'):
        enter_text = ''

        if mode == 'decrypt':
            enter_text = line
        elif mode == 'decryptf':
            try:
                with open(input('decryptf >>> '), mode='r') as f:
                    for i in f:
                        enter_text += i
            except FileNotFoundError as _:
                print('---> File not found!')
                return

        decrypt_offset = self.get_crypt_offset(enter_text)
        list_symbols = []

        for symbol in self.get_real_symbols(enter_text, decrypt_offset):
            list_symbols.append(symbol)

        try:
            list_symbols.pop(-1)
        except IndexError as _:
            print('---> Key not found!')
            return

        decrypt_text = ''
        decrypt_dict = self.get_decrypt_dict(decrypt_offset)

        for crypt_s in list_symbols:
            if crypt_s in decrypt_dict.keys():
                if decrypt_dict[crypt_s].isspace():
                    continue
                decrypt_text += decrypt_dict[crypt_s]

        return decrypt_text


def _console_mode():
    while True:
        crypt = Crypt()
        switch = input('mode[crypt(1) or decrypt(2) or cryptf(3) or decryptf(4) or exit(-1)]: ')
        try:
            if switch == 'crypt' or switch == '1':
                print(crypt.crypt_mode('', mode='crypt'))
            elif switch == 'decrypt' or switch == '2':
                print(crypt.decrypt_mode(mode='decrypt'))
            elif switch == 'cryptf' or switch == '3':
                print(crypt.cryptf_mode())
            elif switch == 'decryptf' or switch == '4':
                print(crypt.decrypt_mode(mode='decryptf'))
            elif switch == 'exit' or switch == '-1':
                print('Exit...')
                break
            else:
                print('There is no such mode of operation...')
        except Exception as e:
            print(f'---> Unknown error! More: {e}')


__all__ = (
    Crypt.__name__,
)

if __name__ == '__main__':
    _console_mode()

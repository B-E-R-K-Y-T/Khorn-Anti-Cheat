import sqlite3

from config import DATABASE_NAME, IGNORE


class Database:
    def __init__(self, path_to_db=DATABASE_NAME):
        self.con = sqlite3.connect(path_to_db)
        self.cur = self.con.cursor()

        self.cur.execute('''
CREATE TABLE IF NOT EXISTS Ignore
(
    Id INTEGER PRIMARY KEY NOT NULL, 
    Item TEXT
);''')
        self.con.commit()

    def save_ignore_item(self, item):
        data = (item, )
        self.cur.execute('''
INSERT INTO Ignore (Item)  
VALUES (?);
''', data)
        self.con.commit()

    def get_ignore_items(self):
        res = self.cur.execute('SELECT * FROM Ignore;')

        return res.fetchall()

    def check_exist_table(self, name_table: str):
        data = (name_table, )
        res = self.cur.execute(f'''
SELECT name FROM sqlite_master WHERE type='table' AND name=?;
''', data)

        if res:
            return True

        return False

    def __del__(self):
        self.cur.close()
        self.con.close()


def add_init_values_to_table(db: Database, name_table: str = 'Ignore'):
    if db.check_exist_table(name_table):
        for value in IGNORE:
            db.save_ignore_item(value)


if __name__ == '__main__':
    add_init_values_to_table(Database('/home/berkyt/PycharmProjects/Khorn/data/Khorn_data.db'))
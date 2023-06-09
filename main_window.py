import threading

from tkinter.ttk import Combobox
from tkinter import *
from tkinter import messagebox
from tools.database_worker import Database
from tools.directory_worker import DirectorySaver, get_my_directory, FileSaver, DirectoryInspector
from tools.exceptions import InvalidDir

DB = Database()


def add_ignore_name_to_db():
    text = str(txt.get())

    if text:
        DB.save_ignore_item(text)
        combo['values'] = DB.get_ignore_items()
    elif text in DB.get_ignore_items():
        messagebox.showerror('Error!', 'Item already exist!')
    else:
        messagebox.showerror('Error!', 'Data is empty!')


def delete_ignore_name_to_db():
    text = str(txt_d.get())

    if text not in DB.get_ignore_items():
        messagebox.showerror('Error!', 'Item not exist!')
        return

    if text:
        DB.save_ignore_item(text)
        combo['values'] = DB.delete_ignore_item(text)
    else:
        messagebox.showerror('Error!', 'Data is empty!')


def listen():
    print('<KHORN> Blood, for the God of blood! Skulls for the throne of skulls!')

    DirectorySaver(get_my_directory(__file__)).save_directory(FileSaver())

    while True:
        d_l = DirectoryInspector(get_my_directory(__file__))
        try:
            d_l.check_valid_file()
        except InvalidDir as ex:
            messagebox.showerror('Error', ex)
            exit()


def init_khorn():
    messagebox.showinfo('Khorn msg', 'Blood, for the God of blood! Skulls for the throne of skulls!')
    
    t = threading.Thread(
    target=listen,
    daemon=True
    )
    t.start()


def init_window():
    window.mainloop()


window = Tk()
window.title("Khorn")
window.geometry('720x480')

lbl = Label(window, text="Add ignore: ")
lbl.grid(column=1, row=0)
txt = Entry(window, width=10)
txt.grid(column=2, row=0)
btn = Button(window, text="Add", command=add_ignore_name_to_db)
btn.grid(column=3, row=0)

btn_k = Button(window, text="KHORN", command=init_khorn)
btn_k.grid(column=4, row=0)

lbl_d = Label(window, text="Delete ignore: ")
lbl_d.grid(column=1, row=1)
txt_d = Entry(window, width=10)
txt_d.grid(column=2, row=1)
btn_d = Button(window, text="Delete", command=delete_ignore_name_to_db)
btn_d.grid(column=3, row=1)

combo = Combobox(window)
combo['values'] = DB.get_ignore_items()
# combo.current(1)  # установите вариант по умолчанию
combo.grid(column=0, row=0)

if __name__ == '__main__':
    init_window()

from time import strftime
from tkinter import messagebox


class CustomFunctions:
    def __init__(self, root):
        self.root = root

    def log_writing(self, response):
        with open('log.txt', 'a', encoding='UTF-8') as log:
            log.write(
                strftime(
                    str("%H:%M:%S %Y-%m-%d") + ' ' + str(response.content) + '\n'))

    def os_error_log(self, e):
        messagebox.showerror(title='Connection error', message=e.args[0].reason)
        #print(e.args[0])
        #print(dir(e.args[0].reason))
        with open('log.txt', 'a', encoding='UTF-8') as log:
            log.write(strftime(str("%H:%M:%S %Y-%m-%d") + str(e.args[0].reason) + '\n'))

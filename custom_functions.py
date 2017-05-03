import locale
import codecs
import sys
from time import strftime
from tkinter import messagebox
import re
import logging


class CustomFunctions:
    def __init__(self, root):
        self.root = root

    logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s', level=logging.DEBUG, filename='log.log',
                        datefmt='%d-%b-%Y %H:%M:%S.000Z')
    #logging.basicConfig(format=u'%(asctime)s%(log.txt)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s',
    #                    level=logging.DEBUG)

    def log_writing(self, response):
        with open('log.txt', 'a', encoding='UTF-8') as log:
            log.write(
                strftime(
                    str("%H:%M:%S %Y-%m-%d") + ' ' + str(response.content) + '\n'))

    def connection_error_log(self, e):
        # Вытащил аргументы из окна ошибки для отображения на warning-окне и сконвертировал в строку
        e_warning = str(e.args[0].reason)
        # Ищу конкретный кусок ошибки для вывода на warning-окне и вырезаю его
        e_lst = re.findall('>:\s(.+)', e_warning)
        # "re" вернул мне список - конвертирую его в строку
        e_str = ''.join(e_lst)
        # Перевел строку в байты
        e_str_unicode = codecs.encode(e_str, 'utf-8')
        e_str_utf = codecs.decode(e_str_unicode, encoding='utf-8')
        messagebox.showerror(title='Connection error', message=e_str)
        logging.critical(e_str)
        #with open('log.txt', 'a', encoding='utf-8') as log:
        #    log.write(strftime("%H:%M:%S %Y-%m-%d") + e_str_utf + '\n')

        '''
        with open('log.txt', 'a', encoding='utf-8') as log:
            log.write(strftime("%H:%M:%S %Y-%m-%d") + e_str_utf + '\n')
        '''
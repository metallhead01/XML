import locale
import codecs
from sys import *
from tkinter import messagebox
import re
import logging.config
import logging

# Указываю имя файла с настройками для внешнего редактирования
logging.config.fileConfig('logging.ini')
# Для вывода в файл
logger = logging.getLogger('xmlParser')


class CustomFunctions:
    def __init__(self, root):
        self.root = root

    #logging.basicConfig(level=logging.DEBUG)

    def app_start(self):
        logger.info('Application Started')

    def app_close(self):
        logger.info('Application Closed')

    def log_writing(self, response):
        self.response = response
        logger.info(self.response)
        #with open('log.txt', 'a', encoding='UTF-8') as log:
        #    log.write(
        #        strftime(
        #            str("%H:%M:%S %Y-%m-%d") + ' ' + str(response.content) + '\n'))

    def connection_error_log(self, e):
        self.e = e
        # Вытащил аргументы из окна ошибки для отображения на warning-окне и сконвертировал в строку
        e_warning = str(self.e.args[0].reason)
        # Ищу конкретный кусок ошибки для вывода на warning-окне и вырезаю его
        e_lst = re.findall('>:\s(.+)', e_warning)
        # "re" вернул мне список - конвертирую его в строку
        e_str = ''.join(e_lst)
        # Перевел строку в байты
        e_str_unicode = codecs.encode(e_str, 'utf-8')
        e_str_utf = codecs.decode(e_str_unicode, encoding='utf-8')
        messagebox.showerror(title='Connection error', message=e_str)
        logger.critical(e_str)
        #with open('log.txt', 'a', encoding='utf-8') as log:
        #    log.write(strftime("%H:%M:%S %Y-%m-%d") + e_str_utf + '\n')

    def debug_log_writing(self, response):
        self.response = response
        logger.debug(self.response)

    def warning_log_writing(self, response):
        self.response = response
        logger.warning(self.response)

    def info_log_writing(self, response):
        self.response = response
        logger.info(self.response)

    def wrong_login_pass(self, response):
        self.response = response
        logger.debug(self.response)
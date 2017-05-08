import requests
import xml.etree.ElementTree as ET
import sqlite3
import logging.config
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import strftime
from custom_functions import *


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('tab2Requests')


class Request:
    def __init__(self, root):
        self.root = root

        # Создаем соединение с нашей базой данных
        db = sqlite3.connect('reference.db')

        # Создаем курсор - это специальный объект который делает запросы и получает их результаты
        cur = db.cursor()

        # Отчистим содержимое БД перед новым запросом
        cur.execute('''DROP TABLE IF EXISTS Order_Type''')
        cur.execute('''DROP TABLE IF EXISTS Tables''')
        cur.execute('''DROP TABLE IF EXISTS Cashes''')
        cur.execute('''DROP TABLE IF EXISTS Currencies''')
        cur.execute('''DROP TABLE IF EXISTS Menu_Order''')
        cur.execute('''DROP TABLE IF EXISTS Menu''')
        cur.execute('''DROP TABLE IF EXISTS Employees''')

        logger.info('DB was cleared.')

        # Создаем таблицы в reference.db
        cur.execute('''CREATE TABLE Order_Type ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, code INTEGER)''')
        cur.execute('''CREATE TABLE Tables ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, code INTEGER)''')
        cur.execute('''CREATE TABLE Cashes ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, code INTEGER)''')
        cur.execute('''CREATE TABLE Currencies ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, ident INTEGER)''')
        cur.execute('''CREATE TABLE Menu_Order ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ident INTEGER, price INTEGER)''')
        cur.execute('''CREATE TABLE Menu ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ident INTEGER, name TEXT)''')
        cur.execute('''CREATE TABLE Employees ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, code INTEGER, name TEXT)''')

        db.close()

        logger.info('New tables in DB were created.')
        logger.info('Here we go!!!')

    def code_list_request(self, string, i, p, user_name, pass_word, table):
        self.string = string
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word
        self.table = table
        # Основное тело запроса
        xml_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "' + self.string + '"/></RK7Query>'
        ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(ip_string, data=xml_request_string, auth=(self.user_name, self.pass_word), verify=False)
        parsed_element_list = ET.fromstring(response.content)
        db = sqlite3.connect('reference.db')
        for item in parsed_element_list.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                # Делаем запрос в DB - переменные в запросе отображаем через: "{}" - для переменной таблицы и
                # "?" - для переменных значений.
                cur = db.cursor()
                cur.execute('''INSERT INTO {} (name, code) VALUES (?, ?)'''.format(self.table), (attr_of_item_node.get('Name'), attr_of_item_node.get('Code')))
                logger.debug('Transaction to "%s" table is completed.' % (attr_of_item_node.get('Name')))
                cur.close()
        db.commit()
        db.close()

    def currencies_list_request(self, string, i, p, user_name, pass_word, table):
        self.string = string
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word
        self.table = table
        # Основное тело запроса
        xml_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "' + self.string + '"/></RK7Query>'
        ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(ip_string, data=xml_request_string, auth=(self.user_name, self.pass_word), verify=False)
        parsed_element_list = ET.fromstring(response.content)
        db = sqlite3.connect('reference.db')
        cur = db.cursor()
        for item in parsed_element_list.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                # Делаем запрос в DB - переменные в запросе отображаем через: "{}" - для переменной таблицы и
                # "?" - для переменных значений.
                cur.execute('''INSERT INTO {} (name, ident) VALUES (?, ?)'''.format(self.table), (attr_of_item_node.get('Name'), attr_of_item_node.get('Ident')))
                logger.debug('Transaction of "%s" item is completed.' % (attr_of_item_node.get('Name')))
        db.commit()
        cur.close()
        db.close()
    def menu_request(self, i, p, user_name, pass_word):
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word
        session = requests.session()
        db = sqlite3.connect('reference.db')
        cur = db.cursor()
        cur.execute('''SELECT code FROM Cashes''')
        # Сформируем переменную для запроса. Почему-то отвалилась конвертация в самом теле запроса, пришлось выделять в
        # отдельную переменную.
        a = str(cur.fetchone()[0])

        ''' Собираем строку для отправки запроса. Для этого вызовем метод "code_list_request" для 
        объекта "collections_request". Этот метод нам понадобится для того, чтобы получить список кодов касс
         (нам нужена хотя бы одна - ее код нужен для создания запроса в поле StationCode)
    
        Аналогично верхним функциям, т.к. функция возвращает нам словарь, выковырем значения с помощью
        стандартной функции .value и сконвертируем полученные значения в список и затем с помощью [0]
        получим первый эелемент списка'''

        xml_request_string = '<RK7Query><RK7CMD CMD="GetOrderMenu" StationCode="' + a + '" DateTime="' + strftime("%Y-%m-%d %H:%M:%S") + '" /></RK7Query>'
        print(xml_request_string)
        cur.close()

        # Делаю запрос всех элементов меню (нужен для получения меню). В дальнейшем будет использоваться для
        # сравнения с запросом "GetRefData".
        xml_request_string_full_menu = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "MENUITEMS"/></RK7Query>'

        ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
        # Убираем warnings об SSL (warnings выводятся даже при отключении SSL)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # Запрос с выключенным SSL
        response = session.request(method='GET', url=ip_string, data=xml_request_string,
                                   auth=(self.user_name, self.pass_word), verify=False)

        parsed_ident_nodes = ET.fromstring(response.content)
        # Перебираем все ноды "Item" в прямой дочерней ноде "Dishes"
        for item in parsed_ident_nodes.findall("./Dishes/Item"):
            # В переменную "attr_of_item_node" передаем значения всех атрибутов (2 штуки)
            attr_of_item_node = (item.attrib)
            cur = db.cursor()
            cur.execute('''INSERT INTO Menu_Order (ident, price) VALUES (?, ?)''',
                             (attr_of_item_node.get('Ident'), attr_of_item_node.get('Price')))
            logger.debug('Transaction of "%s" ident is completed.' % (attr_of_item_node.get('Ident')))
        db.commit()
        cur.close()

        # Делаем запрос полного меню
        response_menu = session.request(method='GET', url=ip_string, data=xml_request_string_full_menu,
                                   auth=(self.user_name, self.pass_word), verify=False)
        logger.info(response)
        # С помощью The ElementTree XML API делаем парсинг ответа из строки
        parsed_full_menu = ET.fromstring(response_menu.content)
        for item in parsed_full_menu.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                cur = db.cursor()
                # Наполним таблицу DB значениями
                cur.execute('''INSERT INTO Menu (name, ident) VALUES (?, ?)''',
                            (attr_of_item_node.get('Name'), attr_of_item_node.get('Ident')))
                logger.info('Transaction of "%s" item is completed.' % (attr_of_item_node.get('Name')))
        db.commit()
        cur.close()
        db.close()

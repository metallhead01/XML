import os
import sys
sys.path.append(os.path.join(sys.path[0], "modules"))
import requests
import xml.etree.ElementTree as ET
import sqlite3
import logging.config
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import strftime
from custom_functions import *
from tkinter import messagebox
from random import randint


logging.config.fileConfig('..\logging.ini')
logger = logging.getLogger('tab2Requests')
# Создали базу данных, если ее нет
with open ('reference.db', 'a') as base:
    logger.info('DB was created.')



class Request:
    def __init__(self, root):
        self.root = root

        # Создаем соединение с нашей базой данных
        self.db = sqlite3.connect('reference.db')

        # Создаем курсор - это специальный объект который делает запросы и получает их результаты
        self.cur = self.db.cursor()

    def code_list_request(self, string, i, p, user_name, pass_word, table):
        self.string = string
        self.i = i
        self.p = p
        # Основное тело запроса
        xml_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "' + string + '"/></RK7Query>'
        ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(ip_string, data=xml_request_string, auth=(user_name, pass_word), verify=False)
        parsed_element_list = ET.fromstring(response.content)
        # Создадим пустой словарь. В нем будем хранить пары "имя-код".
        dict_name_code = {}
        l_ist_code = []
        l_ist_name = []
        for item in parsed_element_list.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                l_ist_code.append(attr_of_item_node.get('Code'))
                l_ist_name.append(attr_of_item_node.get('Name'))
                # Делаем запрос в DB - переменные в запросе отображаем через: "{}" - для переменной таблицы и
                # "?" - для переменных значений.
                #self.cur.execute('''INSERT INTO {} (name, code) VALUES (?, ?)'''.format(table), (attr_of_item_node.get('Name'), attr_of_item_node.get('Code')))
                #logger.debug('Transaction to "%s" table is completed.' % (attr_of_item_node.get('Name')))
                # Собирем словарь из двух списков - l_ist_name будут ключами, l_ist_code - значениями.
                dict_name_code = dict(zip(l_ist_name, l_ist_code))
            #self.db.commit()

        #self.cur.close()
        # Функция вернула словарь
        return dict_name_code

    def menu_request(self, i, p, user_name, pass_word):
        session = requests.session()
        self.i = i
        self.p = p
        get_order_menu_ident = []
        full_menu_ident = []
        prices = []
        names = []
        dict_ident_price = {}
        dict_name_ident = {}
        # Создаем соединение с нашей базой данных
        self.db = sqlite3.connect('reference.db')
        # Создаем курсор - это специальный объект который делает запросы и получает их результаты
        self.cur = self.db.cursor()
        self.cur.execute('''SELECT code FROM Cashes''')

        ''' Собираем строку для отправки запроса. Для этого вызовем метод "code_list_request" для 
        объекта "collections_request". Этот метод нам понадобится для того, чтобы получить список кодов касс
         (нам нужена хотя бы одна - ее код нужен для создания запроса в поле StationCode)
    
        Аналогично верхним функциям, т.к. функция возвращает нам словарь, выковырем значения с помощью
        стандартной функции .value и сконвертируем полученные значения в список и затем с помощью [0]
        получим первый эелемент списка'''

        xml_request_string = \
        '<RK7Query><RK7CMD CMD="GetOrderMenu" StationCode="' + str(self.cur.fetchone()[0]) + '" DateTime="' +\
        strftime("%Y-%m-%d %H:%M:%S") + '" /></RK7Query>'

        # Делаю запрос всех элементов меню (нужен для получения меню). В дальнейшем будет использоваться для
        # сравнения с запросом "GetRefData".
        xml_request_string_full_menu = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "MENUITEMS"/></RK7Query>'

        ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
        # Убираем warnings об SSL (warnings выводятся даже при отключении SSL)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        # Запрос с выключенным SSL
        response = session.request(method='GET', url=ip_string, data=xml_request_string,
                                   auth=(user_name, pass_word), verify=False)

        parsed_ident_nodes = ET.fromstring(response.content)
        # Перебираем все ноды "Item" в прямой дочерней ноде "Dishes"
        for item in parsed_ident_nodes.findall("./Dishes/Item"):
            # В переменную "attr_of_item_node" передаем значения всех атрибутов (2 штуки)
            attr_of_item_node = (item.attrib)
            # Раскладываем по спискам значения атрибутов
            get_order_menu_ident.append(attr_of_item_node.get('Ident'))
            prices.append(attr_of_item_node.get('Price'))
            #self.cur.execute('''INSERT INTO Menu_Order (ident, price) VALUES (?, ?)''',
            #                 (attr_of_item_node.get('Ident'), attr_of_item_node.get('Price')))
            #self.db.commit()
            #logger.info('Transaction of "%s" ident is completed.' % (attr_of_item_node.get('Ident')))
            dict_ident_price = dict(zip(get_order_menu_ident, prices))

        # Делаем запрос полного меню
        response_menu = session.request(method='GET', url=ip_string, data=xml_request_string_full_menu,
                                   auth=(user_name, pass_word), verify=False)
        #logger.info(response)
        # С помощью The ElementTree XML API делаем парсинг ответа из строки
        parsed_full_menu = ET.fromstring(response_menu.content)
        for item in parsed_full_menu.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                full_menu_ident.append(attr_of_item_node.get('Ident'))
                names.append(attr_of_item_node.get('Name'))
                dict_name_ident = dict(zip(full_menu_ident, names))
                # Наполним таблицу DB значениями
                #self.cur.execute('''INSERT INTO Menu (name, ident) VALUES (?, ?)''',
                #(attr_of_item_node.get('Name'), attr_of_item_node.get('Ident')))
                #self.db.commit()
                #logger.info('Transaction of "%s" item is completed.' % (attr_of_item_node.get('Name')))

        #comparing_result = list(set(get_order_menu_ident) & set(full_menu_ident))
        return get_order_menu_ident

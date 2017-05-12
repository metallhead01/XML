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
        cur = db.cursor(mycursor)

        # Отчистим содержимое БД перед новым запросом
        cur.execute('''DROP TABLE IF EXISTS Order_Type''')
        cur.execute('''DROP TABLE IF EXISTS Tables''')
        cur.execute('''DROP TABLE IF EXISTS Cashes''')
        cur.execute('''DROP TABLE IF EXISTS Employees''')
        cur.execute('''DROP TABLE IF EXISTS Employees_2''')
        cur.execute('''DROP TABLE IF EXISTS Currencies''')
        cur.execute('''DROP TABLE IF EXISTS Menu_Order''')
        cur.execute('''DROP TABLE IF EXISTS Menu''')
        cur.execute('''DROP TABLE IF EXISTS Orders''')
        cur.execute('''DROP TABLE IF EXISTS Visits''')

        logger.info('DB was cleared.')

        # Создаем таблицы в reference.db
        cur.execute('''CREATE TABLE Order_Type ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, code INTEGER)''')
        cur.execute('''CREATE TABLE Tables ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, code INTEGER)''')
        cur.execute('''CREATE TABLE Cashes ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, code INTEGER)''')
        cur.execute('''CREATE TABLE Employees ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, role TEXT,
        role_ident INTEGER, name TEXT, card_code INTEGER, ident INTEGER, registered TEXT)''')
        cur.execute('''CREATE TABLE Employees_2 ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, card_code INTEGER, ident INTEGER)''')
        cur.execute('''CREATE TABLE Currencies ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT, ident INTEGER)''')
        cur.execute('''CREATE TABLE Menu_Order ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ident INTEGER, price INTEGER)''')
        cur.execute('''CREATE TABLE Menu ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, ident INTEGER, name TEXT)''')
        cur.execute('''CREATE TABLE Orders ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, visit_id INTEGER, order_id
        INTEGER, order_name INTEGER, order_guid TEXT, table_code INTEGER, waiter_id INTEGER, to_pay_sum INTEGER)''')
        cur.execute('''CREATE TABLE Visits ('key' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, visit_id INTEGER, finished INTEGER)''')

        db.close()

        logger.info('New tables in DB were created.')
        logger.info('Here we go!!!')

    def collections_list_request(self, string, i, p, user_name, pass_word, table):
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
                cur = db.cursor(mycursor)
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
        cur = db.cursor(mycursor)
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

    def employees_list_request(self, i, p, user_name, pass_word):
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word
        # Основное тело запроса
        xml_request_string = ('<RK7Query><RK7CMD CMD="GetRefData" RefName="Restaurants" IgnoreEnums="1" '
                              'WithChildItems="3" WithMacroProp="1" OnlyActive = "1" '
                              'PropMask="RIChildItems.(Ident,Name,genRestIP,genprnStation,genDefDlvCurrency,AltName,'
                              'RIChildItems.TRole(ItemIdent,passdata,Name,AltName,gen*,'
                              'RIChildItems.(Ident,Name,AltName,gen*)))"/></RK7Query>')

        ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(ip_string, data=xml_request_string, auth=(self.user_name, self.pass_word), verify=False)
        parsed_employees_list = ET.fromstring(response.content)
        db = sqlite3.connect('reference.db')
        for item in parsed_employees_list.findall("./RK7Reference/RIChildItems/TRK7Restaurant/RIChildItems/TRole"):
            attr_of_role_node = item.attrib
            # cur = db.cursor(mycursor)
            # cur.execute('''INSERT INTO Employees (role, role_ident) VALUES (?, ?)''', (attr_of_role_node.get('Name'), attr_of_role_node.get('ItemIdent')))
            # logger.debug('Transaction of "%s" role is completed.' % (attr_of_role_node.get('Name')))
            # cur.close()
            # Получим childs для выбранной нами ноды
            if item:
                employees = item[0].getchildren()
                for employee in employees:
                    cur = db.cursor(mycursor)
                    employee_att = employee.attrib
                    cur.execute('''INSERT INTO Employees (role, role_ident, name, ident) VALUES (?, ?, ?, ?)''',
                    (attr_of_role_node.get('Name'), attr_of_role_node.get('ItemIdent'), employee_att.get('Name'),
                    employee_att.get('Ident')))
                    logger.debug('Transaction of "%s" is completed.' % (employee_att.get('Name')))
                    cur.close()

        xml_employees_code_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "Employees"/></RK7Query>'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response_code = requests.get(ip_string, data=xml_employees_code_request_string,
                                auth=(self.user_name, self.pass_word), verify=False)

        parsed_employees_code_list = ET.fromstring(response_code.content)
        cur_2 = db.cursor(mycursor)
        cur_2.execute('''SELECT ident FROM Employees''')

        ident_list = cur_2.fetchall()

        for item in parsed_employees_code_list.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                cur = db.cursor(mycursor)
                cur.execute('''INSERT INTO Employees_2 (card_code, ident) VALUES (?, ?)''', (attr_of_item_node.get('Code'), attr_of_item_node.get('Ident')))
                cur.close()
        # Делаем выборку из таблицы Employees_2 для значений совпадающих ident (Employees.ident = Employees_2.ident)
        cur_2.execute('''UPDATE Employees SET card_code = (SELECT card_code FROM Employees_2 WHERE Employees.ident = Employees_2.ident)''')
        cur_2.close()
        db.commit()


    def menu_request(self, i, p, user_name, pass_word):
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word
        session = requests.session()
        db = sqlite3.connect('reference.db')
        cur = db.cursor(mycursor)
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
            cur = db.cursor(mycursor)
            cur.execute('''INSERT INTO Menu_Order (ident, price) VALUES (?, ?)''',
                             (attr_of_item_node.get('Ident'), attr_of_item_node.get('Price')))
            logger.debug('Transaction of "%s" ident is completed.' % (attr_of_item_node.get('Ident')))
        db.commit()
        cur.close()

        # Делаем запрос полного меню
        response_menu = session.request(method='GET', url=ip_string, data=xml_request_string_full_menu,
                                   auth=(self.user_name, self.pass_word), verify=False)
        # С помощью The ElementTree XML API делаем парсинг ответа из строки
        parsed_full_menu = ET.fromstring(response_menu.content)
        for item in parsed_full_menu.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                cur = db.cursor(mycursor)
                # Наполним таблицу DB значениями
                cur.execute('''INSERT INTO Menu (name, ident) VALUES (?, ?)''',
                            (attr_of_item_node.get('Name'), attr_of_item_node.get('Ident')))
                logger.debug('Transaction of "%s" item is completed.' % (attr_of_item_node.get('Name')))
        db.commit()
        cur.close()
        db.close()

    def order_list_request(self, i, p, user_name, pass_word):
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word
        # Основное тело запроса
        xml_request_string = '<RK7Query><RK7CMD CMD="GetOrderList"/></RK7Query>'
        ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(ip_string, data=xml_request_string, auth=(self.user_name, self.pass_word), verify=False)
        parsed_order_list = ET.fromstring(response.content)
        db = sqlite3.connect('reference.db')
        for item in parsed_order_list.findall("./Visit"):
            attr_of_orders_node = item.attrib
            cur = db.cursor(mycursor)
            cur.execute('''INSERT INTO Visits (visit_id, finished) VALUES (?, ?)''',
            (attr_of_orders_node.get('VisitID'), attr_of_orders_node.get('Finished')))
            logger.debug('Transaction of "%s" visit is completed.' % (attr_of_orders_node.get('VisitID')))
            cur.close()
            # Получим childs для выбранной нами ноды
            orders = item[0].getchildren()
            for order in orders:
                cur = db.cursor(mycursor)
                order_att = order.attrib
                cur.execute('''INSERT INTO Orders (visit_id, order_id, order_name, order_guid, table_code, waiter_id,
                to_pay_sum) VALUES (?, ?, ?, ?, ?, ?, ?)''', (attr_of_orders_node.get('VisitID'),
                order_att.get('OrderID'), order_att.get('OrderName'), order_att.get('guid'), order_att.get('TableCode'),
                order_att.get('WaiterID'), order_att.get('ToPaySum')))
                logger.debug('Transaction of "%s" order is completed.' % (order_att.get('OrderName')))
                cur.close()
        db.commit()
        db.close()

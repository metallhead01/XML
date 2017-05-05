import os
import sys
import time
import requests
import xml.etree.ElementTree as ET
import sqlite3
import logging.config
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import strftime
from custom_functions import *
from random import randint
from tkinter import messagebox


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('stressTesting')


class Stress_functions:
    def __init__(self):

    #def __init__(self, root):
        #self.root = root

        logging.debug('Test sarted.')

    def start_testing(self, i, p, user_name, pass_word, orders_number, hold_time,pay_time):
        # Создаем соединение с нашей базой данных
        db = sqlite3.connect('reference.db')
        # Создаем курсор - это специальный объект который делает запросы и получает их результаты
        cur_1 = db.cursor()
        session = requests.session()
        times = 0
        # Запросим количество строк в таблицах, для того чтобы правильно задать границы случайной генерации чисел.
        # Полученм переменую используем в качестве второго аргумнта функции ".randint".
        cur_1.execute('SELECT Count(key) FROM Order_Type')
        a = cur_1.fetchone()[0]
        cur_1.execute('SELECT Count(key) FROM Tables')
        b = cur_1.fetchone()[0]
        cur_1.execute('SELECT Count(key) FROM Cashes')
        c = cur_1.fetchone()[0]
        cur_1.execute('SELECT Count(key) FROM Menu_Order')
        d = cur_1.fetchone()[0]
        cur_1.execute('SELECT Count(key) FROM Currencies')
        e = cur_1.fetchone()[0]
        cur_1.execute('SELECT Count(key) FROM Employees')
        f = cur_1.fetchone()[0]
        db.close()
        count = 0
        # Т.к. начинаем с первого заказа, то количество раз, полученных от пользователя надо уменьшить на 1.
        while times <= (int(orders_number) - 1):
            db = sqlite3.connect('reference.db')
            cur_1 = db.cursor()
            # Order Type code
            cur_1.execute('SELECT code FROM Order_Type WHERE key = ? ', (randint(1, a),))
            order_type = cur_1.fetchone()[0]
            # Table code
            cur_1.execute('SELECT code FROM Tables WHERE key = ? ', (randint(1, b),))
            table_code = cur_1.fetchone()[0]
            # Station code
            cur_1.execute('SELECT code FROM Cashes WHERE key = ? ', (randint(1, c),))
            station_code = cur_1.fetchone()[0]
            # Dish ID ident
            cur_1.execute('SELECT ident FROM Menu_Order WHERE key = ? ', (randint(1, d),))
            dish_id_1 = cur_1.fetchone()[0]
            cur_1.execute('SELECT ident FROM Menu_Order WHERE key = ? ', (randint(1, d),))
            dish_id_2 = cur_1.fetchone()[0]
            cur_1.execute('SELECT ident FROM Menu_Order WHERE key = ? ', (randint(1, d),))
            dish_id_3 = cur_1.fetchone()[0]
            # Currency code
            cur_1.execute('SELECT ident FROM Currencies WHERE key = ? ', (randint(1, e),))
            currency = cur_1.fetchone()[0]
            # Employees code
            cur_1.execute('SELECT code FROM Employees WHERE key = ? ', (randint(1, f),))
            employee_code = cur_1.fetchone()[0]
            # Quantity (умноженное на 1000, т.к. изначально передается в дробнй форме)
            qty = randint(1, 10) * 1000

            # время ожидания перед выполнением запроса
            time.sleep(int(hold_time))
            xml_request_string = '<?xml version="1.0" encoding="UTF-8"?><RK7Query><RK7CMD CMD="CreateOrder"><Order>' \
                                 '<OrderType code= "' + str(order_type) + '" /><Waiter code="' + str(5046)+\
                                 '"/><Table code= "' + str(table_code) + '" /></Order>''</RK7CMD></RK7Query>'

            ''' Проверим, ввел ли ли пользователь ip и порт, если нет - выдадим ошибку'''
            if not i and not p():
                messagebox.showwarning(title='Error', message="Введите IP-адрес и порт!")

            else:
                ip_string_2 = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
                try:
                    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                    response_create_order = session.request(method='POST', url=ip_string_2, data=xml_request_string,
                                                            auth=(user_name, pass_word), verify=False)

                    parsed_ident_nodes = ET.fromstring(response_create_order.content)
                    '''Перебираем все ноды "Item" в прямой дочерней ноде "Dishes"'''
                    parsed_create_order = parsed_ident_nodes.attrib
                    visit_id = parsed_create_order.get('VisitID')

                    xml_save_order = '<RK7Query><RK7CMD CMD="SaveOrder">' \
                                     '<Order visit="' + \
                                     str(visit_id) + '" orderIdent="256" /><Session><Station code="' + \
                                     str(station_code) + '" />' \
                                     '<Dish id="' + str(dish_id_1) + '" quantity="' + str(qty) + '"></Dish>' \
                                     '<Dish id="' + str(dish_id_2) + '" quantity="' + str(qty) + '"></Dish>' \
                                     '<Dish id="' + str(dish_id_3) + '" quantity="' + str(qty) + '"></Dish>' \
                                     '</Session></RK7CMD></RK7Query>'

                    xml_save_order_string = xml_save_order.encode('utf-8')
                    response_save_order = session.request(method='POST', url=ip_string_2, data=xml_save_order_string,
                                                          auth=(user_name, pass_word), verify=False)
                    #Перекодируем response_save_order в нужную нам кодировку (кириллица поломана)
                    response_save_order.encoding = 'UTF-8'
                    logging.debug(response_save_order.text)
                    #Распарсим полученый ответ для того, чтобы получить GUID только что созданного заказа.
                    parsed_guid_nodes = ET.fromstring(response_save_order.content)
                    parsed_guid = parsed_guid_nodes[0].attrib
                    creator = parsed_guid_nodes[0][0].attrib
                    # время ожидания перед оплатой
                    time.sleep(int(pay_time))

                    cur_1.execute('SELECT Count(key) FROM Currencies')
                    e = cur_1.fetchone()[0]

                    xml_pay_string = '<RK7Query><RK7CMD CMD="PayOrder"><Order guid="' + \
                                     str(parsed_guid.get('guid')) + '"/><Cashier code="' + \
                                     str(5046) + '"/><Station code="' + \
                                     str(station_code) + '"/><Payment id="' + \
                                     str(1) + '" amount="' + str(parsed_guid.get('basicSum')) +\
                                     '"/></RK7CMD></RK7Query>'
                    xml_pay_string = xml_pay_string.encode('utf-8')
                    response_pay_order = session.request(method='POST', url=ip_string_2, data=xml_pay_string,
                                                          auth=(user_name, pass_word), verify=False)

                    parsed_pay_nodes = ET.fromstring(response_pay_order.content)
                    parsed_pay_ok = parsed_pay_nodes.attrib
                    status = parsed_pay_ok.get('Status')
                    if status == 'Ok':
                        count += 1
                    response_pay_order.encoding = 'UTF-8'
                    logging.debug(response_pay_order.text)

                except OSError as e:
                    #error_log = CustomFunctions(root)
                    #error_log.connection_error_log(e)
                    logging.warning(e)
            times += 1
            logging.debug('Orders created "%s", Ok is "%s".' % (times, count))
            db.close()
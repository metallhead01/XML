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
        logging.debug('Test started')

    def start_testing(self, i, p, user_name, pass_word, orders_number, hold_time, pay_time):
        self.i = i
        self.p = p
        self.user_name = user_name
        self.pass_word = pass_word
        self.orders_number = orders_number
        self.hold_time = hold_time
        self.pay_time = pay_time
        log = CustomFunctions('stress_log')
        # Создаем соединение с нашей базой данных
        db = sqlite3.connect('reference.db')
        # Создаем курсор - это специальный объект который делает запросы и получает их результаты
        session = requests.session()
        times = 0
        count = 0
        # Т.к. начинаем с первого заказа, то количество раз, полученных от пользователя надо уменьшить на 1.
        if self.orders_number == 1:
            self.orders_number = 2
        else:
            pass
        ''' Проверим, ввел ли ли пользователь ip и порт, если нет - выдадим ошибку'''
        if not self.i and not self.p:
            messagebox.showwarning(title='Error', message="Введите IP-адрес и порт!")
        elif not self.user_name and not self.pass_word:
            messagebox.showwarning(title='Error', message="Введите логин и пароль!")
        elif not self.orders_number and not self.hold_time and not self.pay_time:
            messagebox.showwarning(title='Error', message="Заполните параметры тестирования!")
        else:
            ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
            error_log = CustomFunctions('err_log')
            try:
                # Сделаем простой запрос - "GetRefList" для проверки логина и пароля. Если сервер вернет
                # "401 Unauthorized" - логин или пароль неверен
                xml_request_string = '<RK7Query><RK7CMD CMD="GetRefList"/></RK7Query>'
                ip_string = 'https://' + self.i + ":" + self.p + '/rk7api/v0/xmlinterface.xml'
                requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                response = requests.get(ip_string, data=xml_request_string, auth=(self.user_name, self.pass_word),
                                        verify=False)
                # Если сервер доступен, смотрим на ответ запроса "GetRefList"
                # Если в ответе от сервера есть строка "401 Unauthorized", поднимаем исключение
                if response.text == '<HTML><BODY><B>401 Unauthorized</B></BODY></HTML>':
                    raise NameError('Login or password is incorrect!')
            except requests.ConnectionError as e:
                error_log.connection_error_log(e)
            except NameError:
                messagebox.showerror(title='Connection error', message='Login or password is incorrect!')
                error_log.warning_log_writing('Login or password is incorrect.')
            else:
                # Если такой строки нет - продолжаем выполнение функции
                    try:
                        while times <= (int(self.orders_number) - 1):
                            cur_1 = db.cursor(mycursor)
                            # Order Type code
                            cur_1.execute('SELECT code FROM Order_Type ORDER BY RANDOM() LIMIT 1')
                            order_type = cur_1.fetchone()[0]
                            # Table code
                            cur_1.execute('SELECT code FROM Tables ORDER BY RANDOM() LIMIT 1')
                            table_code = cur_1.fetchone()[0]
                            # Station code
                            cur_1.execute('SELECT code FROM Cashes ORDER BY RANDOM() LIMIT 1')
                            station_code = cur_1.fetchone()[0]
                            # Employees code
                            cur_1.execute('SELECT card_code FROM Employees WHERE NOT role="Дилеры" AND NOT '
                                          'role="Системная" AND NOT role="Web-Reservation" ORDER BY RANDOM() LIMIT 1')
                            # В employee_code положим key и ident, полученные и таблицы employees
                            employee_card_code= cur_1.fetchone()[0]
                            # Currency code
                            cur_1.execute('SELECT ident FROM Currencies ORDER BY RANDOM() LIMIT 1')
                            currency= cur_1.fetchone()[0]
                            cur_1.close()

                            # Время ожидания перед выполнением запроса
                            time.sleep(int(self.hold_time))
                            # Регистрируем пользователя
                            xml_register_waiter_string = '<RK7Query><RK7CMD CMD="LoginOnStation" cardCode = "' + \
                                                         str(employee_card_code) + '"><Station code = "' +\
                                                         str(station_code) + '"/></RK7CMD></RK7Query>'
                            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                            xml_unicode_register_waiter_string = xml_register_waiter_string.encode('utf-8')
                            response_register_waiter = session.request(method='POST', url=ip_string,
                                                                       data=xml_unicode_register_waiter_string,
                                                                       auth=(self.user_name, self.pass_word),
                                                                       verify=False)
                            response_register_waiter.encoding = 'UTF-8'
                            log.debug_log_writing(response_register_waiter.text)

                            if 'Status="Ok"' in response_register_waiter.text:
                                cur_1 = db.cursor(mycursor)
                                user_registred = cur_1.execute('''UPDATE Employees SET registered="yes" WHERE card_code
                                =(?) ''', (employee_card_code,))
                                log.debug_log_writing(user_registred)
                            cur_1.close()

                            xml_request_string = ('<?xml version="1.0" encoding="UTF-8"?><RK7Query>'
                            '<RK7CMD CMD="CreateOrder"><Order><OrderType code= "' + str(order_type) + '" />'
                            '<Waiter code="' + str(employee_card_code) + '"/><Table code= "' + str(table_code) + '" />'
                            '</Order></RK7CMD></RK7Query>')
                            xml_unicode_request_string = xml_request_string.encode('utf-8')
                            response_create_order = session.request(method='POST', url=ip_string,
                                                                    data=xml_unicode_request_string,
                                                                    auth=(self.user_name, self.pass_word), verify=False)
                            response_create_order.encoding = 'UTF-8'
                            log.debug_log_writing(response_create_order.text)
                            parsed_ident_nodes = ET.fromstring(response_create_order.content)
                            '''Перебираем все ноды "Item" в прямой дочерней ноде "Dishes"'''
                            parsed_create_order = parsed_ident_nodes.attrib
                            # Проверяем возможность создания заказа - если статус что-нибудь, кроме "Ок" кидаем исключение.
                            if parsed_create_order.get('Status') != "Ok":
                                raise NameError(parsed_create_order.get('ErrorText'))
                            # Парсим ID визита
                            visit_id = parsed_create_order.get('VisitID')
                            # Генерируем блюда для запроса. Делаем счетчик количества итераций равным 0.
                            times = 1
                            # Задаем переменную в которой будет храниться количество блюд = rand (не более пяти).
                            a = randint(1, 5)
                            # Задаем пустой словарь, в котором будем хранить коды полученных блюд и их количество.
                            code_qty_dict = {}
                            # Пока количество итераций меньше или равно случайного числа "a", выполнять код.
                            while times <= a:
                                cur_1 = db.cursor()
                                # Взяли раздомное значение из базы
                                cur_1.execute('SELECT ident FROM Menu_Order ORDER BY RANDOM() LIMIT 1')
                                dish_id = cur_1.fetchone()[0]
                                # Добавили в словарь, quantity (умноженное на 1000, т.к. изначально передается в
                                # дробной форме)
                                code_qty_dict[str(dish_id)] = (randint(1, 10) * 1000)
                                times += 1
                            l_ist = []
                            # Собираем строку для XML-запроса. Для этого значения из словаря вставляем в шаблон и
                            # добавляем в список
                            for key, value in code_qty_dict.items():
                                l_ist.append('<Dish id= "' + str(key) + '" quantity= "' + str(value) + '"></Dish>')
                            # Объединяем список в строку при помощи разделителя
                            sep = ' + '
                            sep.join(l_ist)
                            # Обнулили счетчик (т.к. мы находимся в глобальном цикле while)
                            times = 1
                            cur_1.close()
                            xml_save_order = ('<RK7Query><RK7CMD CMD="SaveOrder"><Order visit="' + str(visit_id) + '" '
                            'orderIdent="256" /><Session><Station code="' + str(station_code) + '" />' + sep.join(l_ist)
                            + '</Session></RK7CMD></RK7Query>')

                            xml_save_order_string = xml_save_order.encode('utf-8')
                            response_save_order = session.request(method='POST', url=ip_string, data=xml_save_order_string,
                                                                  auth=(self.user_name, self.pass_word), verify=False)
                            # Перекодируем response_save_order в нужную нам кодировку (кириллица поломана)
                            response_save_order.encoding = 'UTF-8'
                            log.debug_log_writing(response_save_order.text)
                            # Распарсим полученый ответ для того, чтобы получить GUID только что созданного заказа.
                            parsed_guid_nodes = ET.fromstring(response_save_order.content)

                            '''Обработаем возможное исключение при сохранении заказа'''
                            if parsed_guid_nodes.get('Status') != "Ok":
                                raise NameError(parsed_guid_nodes.get('ErrorText'))
                            parsed_guid = parsed_guid_nodes[0].attrib
                            waiter = parsed_guid_nodes[1][0].attrib

                            # время ожидания перед оплатой
                            time.sleep(int(self.pay_time))

                            cur_1 = db.cursor()
                            cur_1.execute('SELECT Count(key) FROM Currencies')
                            e = cur_1.fetchone()[0]
                            xml_pay_string = ('<RK7Query><RK7CMD CMD="PayOrder"><Order guid="' +
                                             str(parsed_guid.get('guid')) + '"/><Cashier code="' +
                                             str(waiter.get('id')) + '"/><Station code="' +
                                             str(station_code) + '"/><Payment id="' + str(1) + '" amount="' +
                                             str(parsed_guid.get('basicSum'))+'"/></RK7CMD></RK7Query>')
                            xml_pay_string = xml_pay_string.encode('utf-8')
                            try:
                                response_pay_order = session.request(method='POST', url=ip_string, data=xml_pay_string,
                                                                     auth=(self.user_name, self.pass_word),
                                                                     verify=False)
                                parsed_pay_nodes = ET.fromstring(response_pay_order.content)
                                parsed_pay_ok = parsed_pay_nodes.attrib
                                status = parsed_pay_ok.get('Status')
                                if status == 'Ok':
                                    count += 1
                                response_pay_order.encoding = 'UTF-8'
                                log.debug_log_writing(response_pay_order.text)
                                cur_1.close()
                                times += 1
                                if parsed_pay_ok.get('Status') != "Ok":
                                    raise NameError(parsed_pay_ok.get('ErrorText'))
                            except NameError as m:
                                messagebox.showerror(title='Order pay error', message=m)
                                error_log.warning_log_writing(m)
                            else:
                                log.info_log_writing('Orders tried to create "%s", Ok is "%s".' % (times, count))
                                db.close()
                    except NameError as n:
                        messagebox.showerror(title='Order creation error', message=n)
                        error_log.warning_log_writing(n)
                        db.close()

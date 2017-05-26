import requests
import xml.etree.ElementTree as ET
from lxml import etree
import sqlite3
import logging.config
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from time import strftime
from custom_functions import *
from random import randint
i = '172.22.3.86'
p = '4545'
user_name = 'Admin'
pass_word = '1'
ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
db = sqlite3.connect('reference.db')
cur_1 = db.cursor(mycursor)
times = 1
a = randint(1, 10)
code_qty_dict = {}
xml_request_string = ('<?xml version="1.0" encoding="UTF-8"?><RK7Query>'
                      '<RK7CMD CMD="CreateOrder"><Order><OrderType code= "' + str(1) + '" />'
'<Waiter code="' + str(9999) + '"/><Table code= "' + str(1243) + '" />'
                                                             '</Order></RK7CMD></RK7Query>')
xml_unicode_request_string = xml_request_string.encode('utf-8')
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
response_create_order = requests.post(url=ip_string, data=xml_unicode_request_string, auth=(user_name, pass_word), verify=False)
response_create_order.encoding = 'UTF-8'
parsed_ident_nodes = ET.fromstring(response_create_order.content)
'''Перебираем все ноды "Item" в прямой дочерней ноде "Dishes"'''
parsed_create_order = parsed_ident_nodes.attrib
# Проверяем возможность создания заказа - если статус что-нибудь, кроме "Ок" кидаем исключение.
if parsed_create_order.get('Status') != "Ok":
    raise NameError(parsed_create_order.get('ErrorText'))
# Парсим ID визита
visit_id = parsed_create_order.get('VisitID')
dish_id_count = 0
while times <= a:
    # Взяли раздомное значение из базы
    cur_1.execute('SELECT ident FROM Menu_Order ORDER BY RANDOM() LIMIT 1')
    dish_id = cur_1.fetchone()[0]
    cur_1.execute('''SELECT modi_scheme FROM Menu_Order WHERE ident=(?)''', (dish_id,))
    modi_scheme = cur_1.fetchone()[0]
    dish_qty_int = randint(1, 10) * 1000
    if modi_scheme != 0:
        # Запросили modi_group_ident
        cur_1.execute('''SELECT modi_group_ident,down_limit,use_down_limit FROM Modi_Schemes_Groups WHERE modi_scheme_ident=(?)''', (modi_scheme,))

        '''Получили список групп моди для этой моди-схемы с кортежами со значениями modi_group_ident (0), down_limit(1)
        и use_down_limit(2). Пример - [(1000298, 1, 1), (1000299, 1, 1), (1000296, 1, 1)], в одной схеме три группы '''

        modi_group_ident = cur_1.fetchall()
        print(modi_group_ident)
        # Проверяем содержимое списка со всеми комбо-группами данной схемы на обязательные моди.
        for tuple_of_modi_attribs in modi_group_ident:
            # Проверяем, что down_limit больше одного и use_down_limit не равно 0, т.е. моди обязателен к использовани
            if tuple_of_modi_attribs[1] > 0 and tuple_of_modi_attribs[2] != 0:
                # Запросом к Modi_Items нашли моди ID по найденной ранее группе
                cur_1.execute('''SELECT modi_ident FROM Modi_Items WHERE main_parent_ident=(?)''', (tuple_of_modi_attribs[0],))
                modi_ident = cur_1.fetchone()
                # Вставил в SQLite блюда с модификаторами
                cur_1.execute('''INSERT INTO My_Orders (dish_id, dish_qty, modi_id, modi_qty_int) VALUES (?, ?, ?, ?)''',
                              (dish_id, dish_qty_int, modi_ident[0], tuple_of_modi_attribs[1]))
                db.commit()
            dish_id_count += 1
            cur_1.execute('UPDATE My_Orders SET dish_number =(?) WHERE dish_number ISNULL', (dish_id_count,))
            db.commit()
    else:
        cur_1.execute('''INSERT INTO My_Orders (dish_id, dish_qty) VALUES (?, ?)''',
                      (dish_id, dish_qty_int))
        db.commit()
    times += 1
l_ist = []
# Собираем строку для XML-запроса. Для этого значения из словаря вставляем в шаблон и обавляем в список.
cur_1.execute('''SELECT dish_id,dish_qty,modi_id,modi_qty_int FROM My_Orders WHERE modi_id NOTNULL AND order_name ISNULL''')
dishes_with_modi = cur_1.fetchall()
print(dishes_with_modi)
for dish_with_modi in dishes_with_modi:
    l_ist.append('<Dish id= "' + str(dish_with_modi[0]) + '" quantity= "' + str(dish_with_modi[1]) + '">'
                 '<Modi id="' + str(dish_with_modi[2])+ '" count="' + str(dish_with_modi[3]) + '" price="0"/></Dish>')
cur_1.execute('''SELECT dish_id,dish_qty FROM My_Orders WHERE modi_id ISNULL AND order_name ISNULL''')
dishes_without_modi = cur_1.fetchall()
#print(dishes_without_modi)
for key in dishes_without_modi:
    l_ist.append('<Dish id= "' + str(key[0]) + '" quantity= "' + str(key[1]) + '"/></Dish>')
sep = ''
sep.join(l_ist)
# Обнулили счетчик (т.к. мы находимся в глобальном цикле while)
times = 1
cur_1.close()
xml_save_order = ('<RK7Query><RK7CMD CMD="SaveOrder"><Order visit="' + str(visit_id) + '" orderIdent="256" /><Session><Station code="' + str(1) + '" />' +
                  '<Creator code="' + str(9999) + '"/>' + sep.join(l_ist) +
                  '</Session></RK7CMD></RK7Query>')
#print(xml_save_order)
xml_save_order_string = xml_save_order.encode('utf-8')
try:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    response_save_order = requests.post(url=ip_string, data=xml_save_order_string, auth=(user_name, pass_word), verify=False)
    # Перекодируем response_save_order в нужную нам кодировку (кириллица поломана)
    response_save_order.encoding = 'UTF-8'
    # Распарсим полученый ответ для того, чтобы получить GUID только что созданного заказа.
    parsed_guid_nodes = ET.fromstring(response_save_order.content)
    '''Обработаем возможное исключение при сохранении заказа'''
    if parsed_guid_nodes.get('Status') != "Ok":
        raise NameError(parsed_guid_nodes.get('ErrorText'))
    parsed_guid = parsed_guid_nodes[0].attrib
    print(parsed_guid)
    waiter = parsed_guid_nodes[0][1].attrib
    print(parsed_guid.get('OrderName'))
    cur_1.execute('UPDATE My_Orders SET order_name =(?)', (parsed_guid.get('OrderName')))
    db.commit()
except NameError as e:
    print(e)
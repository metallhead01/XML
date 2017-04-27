import unittest
from tkinter import *
from tkinter import ttk
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET
from time import gmtime, strftime

'''
class Request():
    def __init__(self,root):
        self.root = root
'''

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #def tab_2_fields_request(self, string, i, p):
    def test_strings_a_3(self, string, i, p):
        self.string = string
        self.i = i
        self.p = p
        # Основное тело запроса
        xml_request_string = '<RK7Query><RK7CMD CMD="' + string + '"/></RK7Query>'
        xml_unicode_request_string = xml_request_string.encode('utf-8')
        ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(ip_string, data=xml_unicode_request_string, auth=('Admin', '1'), verify=False)

        n = 1
        # self.text_field.delete(1.0, END)

        parsed_order_nodes = ET.fromstring(response.content)
        for item in parsed_order_nodes.findall("./Visit"):
            visit = item.attrib
            self.assertIsNotNone(visit)
            if item[0].tag == "Guests":
                order = item[1][0].attrib
                if visit.get('Finished') == '0':
                    print(str(n) + ". " + "Визит (ID) = " + visit.get(
                        'VisitID') + "\n" + "Завершен= " + visit.get(
                        'Finished') + "\n" + "Количество гостей = " + visit.get(
                        'GuestsCount') + "\n" + "-" * 47 + "\n" + "ID заказа = " + order.get(
                        'OrderID') + "\n" + "Имя заказа = " + order.get(
                        'OrderName') + "\n" + "GUID = " + order.get(
                        'guid') + "\n" "Стол (ID) = " + order.get(
                        'TableID') + "\n" + "Стол (Код) = " + order.get(
                        'TableCode') + "\n" + "Категория Заказа (ID) = " + order.get(
                        'OrderCategID') + "\n" + "Категория заказа (Код) = " + order.get(
                        'OrderCategCode') + "\n" + "Тип Заказа (ID) = " + order.get(
                        'OrderTypeID') + "\n" + "Тип Заказа(Код) = " + order.get(
                        'OrderTypeCode') + "\n" + "Официант (ID) = " + order.get(
                        'WaiterID') + "\n" + "Официант (код) = " + order.get(
                        'WaiterCode') + "\n" + "Сумма заказа = " + order.get(
                        'OrderSum') + "\n" + "Сумма к оплате = " + order.get(
                        'ToPaySum') + "\n" + "PriceListSum = " + order.get(
                        'PriceListSum') + "\n" + "Всего блюд = " + order.get(
                        'TotalPieces') + "\n" + "Счет = " + order.get(
                        'Bill') + "\n" + "Открыт = " + order.get(
                        'CreateTime') + "\n" + "=" * 47 + "\n")
                    n += 1

                elif visit.get('Finished') == '1':

                    print(str(n) + ". " +
                        "Визит (ID) = " + visit.get('VisitID') + "\n" +
                        "Завершен= " + visit.get('Finished') + "\n" +
                        "Количество гостей = " + visit.get(
                        'GuestsCount') + "\n" + "-" * 47 + "\n" +
                        "ID заказа = " + order.get(
                        'OrderID') + "\n" + "Имя заказа = " + order.get(
                        'OrderName') + "\n" + "GUID = " + order.get(
                        'guid') + "\n" "Стол (ID) = " + order.get(
                        'TableID') + "\n" + "Стол (Код) = " + order.get(
                        'TableCode') + "\n" + "Категория Заказа (ID) = " + order.get(
                        'OrderCategID') + "\n" + "Категория заказа (Код) = " + order.get(
                        'OrderCategCode') + "\n" + "Тип Заказа (ID) = " + order.get(
                        'OrderTypeID') + "\n" + "Тип Заказа(Код) = " + order.get(
                        'OrderTypeCode') + "\n" + "Официант (ID) = " + order.get(
                        'WaiterID') + "\n" + "Официант (код) = " + order.get(
                        'WaiterCode') + "\n" + "Сумма заказа = " + order.get(
                        'OrderSum') + "\n" + "Сумма к оплате = " + order.get(
                        'ToPaySum') + "\n" + "PriceListSum = " + order.get(
                        'PriceListSum') + "\n" + "Всего блюд = " + order.get(
                        'TotalPieces') + "\n" + "Счет = " + order.get(
                        'Bill') + "\n" + "Открыт = " + order.get(
                        'CreateTime') + "\n" + "Завершен = " + order.get(
                        'FinishTime') + "\n" + "=" * 47 + "\n")
                    n += 1

            elif item[0].tag == "Orders":
                order = item[0][0].attrib
                if visit.get('Finished') == '0':
                    print(str(n) + ". " + "Визит (ID) = " + visit.get(
                        'VisitID') + "\n" + "Завершен= " + visit.get(
                        'Finished') + "\n" + "Количество гостей = " + visit.get(
                        'GuestsCount') + "\n" + "-" * 47 + "\n" + "ID заказа = " + order.get(
                        'OrderID') + "\n" + "Имя заказа = " + order.get(
                        'OrderName') + "\n" + "GUID = " + order.get(
                        'guid') + "\n" "Стол (ID) = " + order.get(
                        'TableID') + "\n" + "Стол (Код) = " + order.get(
                        'TableCode') + "\n" + "Категория Заказа (ID) = " + order.get(
                        'OrderCategID') + "\n" + "Категория заказа (Код) = " + order.get(
                        'OrderCategCode') + "\n" + "Тип Заказа (ID) = " + order.get(
                        'OrderTypeID') + "\n" + "Тип Заказа(Код) = " + order.get(
                        'OrderTypeCode') + "\n" + "Официант (ID) = " + order.get(
                        'WaiterID') + "\n" + "Официант (код) = " + order.get(
                        'WaiterCode') + "\n" + "Сумма заказа = " + order.get(
                        'OrderSum') + "\n" + "Сумма к оплате = " + order.get(
                        'ToPaySum') + "\n" + "PriceListSum = " + order.get(
                        'PriceListSum') + "\n" + "Всего блюд = " + order.get(
                        'TotalPieces') + "\n" + "Счет = " + order.get(
                        'Bill') + "\n" + "Открыт = " + order.get(
                        'CreateTime') + "\n" + "=" * 47 + "\n")
                    n += 1

                elif visit.get('Finished') == '1':
                    print(str(n) + ". " +
                                                 "Визит (ID) = " + visit.get('VisitID') + "\n" +
                                                 "Завершен= " + visit.get('Finished') + "\n" +
                                                 "Количество гостей = " + visit.get(
                        'GuestsCount') + "\n" + "-" * 47 + "\n" +
                                                 "ID заказа = " + order.get(
                        'OrderID') + "\n" + "Имя заказа = " + order.get(
                        'OrderName') + "\n" + "GUID = " + order.get(
                        'guid') + "\n" "Стол (ID) = " + order.get(
                        'TableID') + "\n" + "Стол (Код) = " + order.get(
                        'TableCode') + "\n" + "Категория Заказа (ID) = " + order.get(
                        'OrderCategID') + "\n" + "Категория заказа (Код) = " + order.get(
                        'OrderCategCode') + "\n" + "Тип Заказа (ID) = " + order.get(
                        'OrderTypeID') + "\n" + "Тип Заказа(Код) = " + order.get(
                        'OrderTypeCode') + "\n" + "Официант (ID) = " + order.get(
                        'WaiterID') + "\n" + "Официант (код) = " + order.get(
                        'WaiterCode') + "\n" + "Сумма заказа = " + order.get(
                        'OrderSum') + "\n" + "Сумма к оплате = " + order.get(
                        'ToPaySum') + "\n" + "PriceListSum = " + order.get(
                        'PriceListSum') + "\n" + "Всего блюд = " + order.get(
                        'TotalPieces') + "\n" + "Счет = " + order.get(
                        'Bill') + "\n" + "Открыт = " + order.get(
                        'CreateTime') + "\n" + "Завершен = " + order.get(
                        'FinishTime') + "\n" + "=" * 47 + "\n")
                    n += 1


if __name__ == "__main__":
    unittest.main('GetOrderList','172.22.3.86','4545')

#root = Tk()
#response = Request(root)
#print(response.tab_2_fields_request('GetOrderList','172.22.3.86','4545'))

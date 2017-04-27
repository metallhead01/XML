'''http://pep8.ru/doc/dive-into-python-3/14.html'''

import xml.etree.ElementTree as ET
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from xml.dom import minidom
from xml.dom.minidom import parse, Node
from time import gmtime, strftime
import xml.etree.ElementTree as etree


session = requests.session()
i = "172.22.3.86"
p = '4545'
'''
# Основное тело запроса
xml_request_string = '<RK7Query><RK7CMD CMD="GetOrderMenu" StationCode="1" DateTime=""/></RK7Query>'
ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
response = requests.get(ip_string, data=xml_request_string, auth=('Admin', '1'),verify=False)
# print(response.content)

parsed_ident_nodes = ET.fromstring(response.content)
idents = []
prices = []
for item in parsed_ident_nodes.findall("./Dishes/Item"):
    attr_of_item_node= (item.attrib)
    idents.append(attr_of_item_node.get('Ident'))
    prices.append(attr_of_item_node.get('Prices'))
'''
# Основное тело запроса
xml_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "Cashes"/></RK7Query>'
ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
response = requests.get(ip_string, data=xml_request_string, auth=('Admin', '1'),verify=False)
#print(response.content)
parsed_cashes_list = ET.fromstring(response.content)
l_ist = []
for item in parsed_cashes_list.findall("./RK7Reference/Items/Item"):
    attr_of_item_node = (item.attrib)
    if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
        l_ist.append(attr_of_item_node.get('Code'))

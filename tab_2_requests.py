import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from xml.dom import minidom
import xml.etree.ElementTree as ET
from time import gmtime, strftime
class Request():
    def __init__(self, root):
        self.root = root

    def tab_2_fields_request(self, string, i, p):
        self.string = string
        self.i = i
        self.p = p
        # Основное тело запроса
        xml_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "' + string + '"/></RK7Query>'
        ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(ip_string, data=xml_request_string, auth=('Admin', '1'), verify=False)
        # print(response.content)
        parsed_cashes_list = ET.fromstring(response.content)
        l_ist = []
        for item in parsed_cashes_list.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                l_ist.append(attr_of_item_node.get('Code'))

        return l_ist

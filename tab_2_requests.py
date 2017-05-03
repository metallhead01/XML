import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xml.etree.ElementTree as ET


class Request:
    def __init__(self, root):
        self.root = root
        self.l_ist_name = []

    def code_list_request(self, string, i, p, user_name, pass_word):
        self.string = string
        self.i = i
        self.p = p
        # Основное тело запроса
        xml_request_string = '<RK7Query><RK7CMD CMD="GetRefData" RefName = "' + string + '"/></RK7Query>'
        ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(ip_string, data=xml_request_string, auth=(user_name, pass_word), verify=False)
        parsed_element_list = ET.fromstring(response.content)
        l_ist_code = []
        for item in parsed_element_list.findall("./RK7Reference/Items/Item"):
            attr_of_item_node = (item.attrib)
            if attr_of_item_node.get('Status') == 'rsActive' and attr_of_item_node.get('ActiveHierarchy') == 'true':
                l_ist_code.append(attr_of_item_node.get('Code'))
                self.l_ist_name.append(attr_of_item_node.get('Name'))

        return l_ist_code

    def name_list_request(self):
        return self.l_ist_name
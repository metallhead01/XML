# coding: utf8


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from xml.dom import minidom


# Используем установку сессий для keep-alive подключений вместо единомоментных выззовов (Use session for keep-alive
# connections).
session = requests.session()

def request():
    try:
        # Получаем аргументы запроса
        #a1 = xml_arg1.get()
        a1 = entry_xml_request_arg1.get()
        a2 = xml_arg2.get()
        a3 = xml_arg3.get()
        a4 = xml_arg4.get()
        a5 = xml_arg5.get()
        i = ip_add.get()
        p = port.get()
        a_full = a1 + a2 + a3

        # Основное тело запроса
        xml_request_string = '<?xml version="1.0" encoding="UTF-8"?><RK7Query> <RK7CMD CMD="' + str(a1) + '" /></RK7Query>'
        ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'

        # Убираем warnings об SSL (warnings выводятся даже при отключении SSL)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # Старый запрос без поддержки keep-alive
        #response = requests.get(ip_string, data=a, auth=('admin', '1'),verify=False)

        # Запрос с выключенным SSL
        response = session.request(method='GET', url=ip_string, data=xml_request_string, auth=('admin', '1'), verify=False)

        xmldoc = minidom.parseString(response.text)
        xmldoc.normalize()

        if a1 == "GetOrderList":
            i = 1
            y = 1
            # Обратимся к тегу Order
            text_field.delete(1.0, END)
            orders = xmldoc.getElementsByTagName("Order")
            # Обратимся к тегу Visit
            visits = xmldoc.getElementsByTagName("Visit")
            for visit in visits:
                text_field.insert(1.0, (str(i) + ". " + "Визит (ID) = " + visit.attributes.item(0).value + "\n" + "Завершен"
                " = " + visit.attributes.item(2).value + "\n" "Количество гостей = " + visit.attributes.item(3).value + "\n"
                + "-"*47 + "\n"))
                i = i + 1
            for order in orders:
                text_field.insert(1.0, (str(y) + ". " + "Имя заказа = " + order.attributes.item(1).value + "\n"
                + "GUID = " + order.attributes.item(5).value + "\n" "Стол (ID) = " + order.attributes.item(6).value + "\n"
                + "Стол (Код) = " + order.attributes.item(7).value + "\n" + "Категория Заказа (ID) = " + order.attributes.
                item(8).value + "\n" + "Категория заказа (Код) = " + order.attributes.item(9).value + "\n"+ "Тип Заказа (ID)"
                " = " + order.attributes.item(10).value + "\n" + "Тип Заказа(Код) = " + order.attributes.item(11).value +
                "\n"+ "Официант (ID) = " + order.attributes.item(12).value + "\n" + "Официант (код) = " + order.attributes
                .item(13).value + "\n" + "Сумма заказа = " + order.attributes.item(14).value + "\n" + "Сумма к оплате = "
                + order.attributes.item(15).value + "\n" + "PriceListSum = " + order.attributes.item(16).value + "\n" +
                "Всего блюд = " + order.attributes.item(17).value + "\n" + "Завершен = " + order.attributes.item(18).value
                + "\n" + "Счет = " + order.attributes.item(19).value + "\n" + "Открыт = " + order.attributes.item(20).value
                + "\n" + "-"*47 + "\n"))
                y = y + 1


        elif a1 == "GetWaiterList":
            text_field.delete(1.0, END)
            waiters = xmldoc.getElementsByTagName("waiter")
            for waiter in waiters:
                text_field.insert(1.0, ("Официант (ID) = " + waiter.attributes.item(0).value + "\n" + "Официант (Код)= " +
                waiter.attributes.item(1).value + "\n" + "-"*47 + "\n"))

        elif a1 == "GetRefList":
            text_field.delete(1.0, END)
            references= xmldoc.getElementsByTagName("RK7Reference")
            for reference in references:
                text_field.insert(1.0, ("RefName = " + reference.attributes.item(0).value + " " + "Count = " + reference.
                attributes.item(1).value + " " + "DataVersion = " + reference.attributes.item(2).value + "\n" + "-"*60 + "\n"))

        else:
            text_field.delete(1.0, END)
            text_field.insert(1.0, response.content)

    except OSError as e:
        print(e)
        messagebox.showerror(title='Connection error', message=e)

    #return(soup)

def create():
    xml_request_string = '<?xml version="1.0" encoding="UTF-8"?><RK7Query><RK7CMD CMD="CreateOrder"><Order><OrderType' \
                         ' code= "' + str(entry_xml_create_tab_2_arg1.get()) + '" /><Table code= "' + \
                         str(entry_xml_create_tab_2_arg2.get()) + '" /></Order></RK7CMD></RK7Query>'
    i_2 = ip_add_2.get()
    #i_2 = '172.22.3.86'
    p_2 = port_2.get()
    #p_2='4545'

    ip_string_2 = 'https://' + i_2 + ":" + p_2 + '/rk7api/v0/xmlinterface.xml'
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response_create_order = session.request(method='POST', url=ip_string_2 , data=xml_request_string, auth=('admin', '1'), verify=False)
        # response_2 = requests.post(ip_string_2, data=xml_request_string, auth=('admin', '1'),verify=False)
        # print(response_create_order.content)
        xmldoc = minidom.parseString(response_create_order.text)
        xmldoc.normalize()
        visitid = xmldoc.getElementsByTagName("RK7QueryResult")
        for visit in visitid:
            visit = visit.attributes.item(5).value
            xml_save_order = '<RK7Query><RK7CMD CMD="SaveOrder" deferred="1" dontcheckLicense="1"><Order visit="' +\
                             str(visit) + '" orderIdent="256" /><Session><Station code="' + \
                             str(entry_xml_create_tab_2_arg3.get()) + '" /><Dish code="' + \
                             str(entry_xml_create_tab_2_arg4.get()) + '" quantity="' + \
                             str(entry_xml_create_tab_2_arg4.get()) + '"></Dish></Session></RK7CMD></RK7Query>'

            xml_save_order_string  = xml_save_order.encode('utf-8')
            response_save_order = session.request(method='POST', url=ip_string_2, data=xml_save_order_string, auth=('admin', '1'), verify=False)
            # Перекодируем response_save_order в нужную нам кодировку (кириллица поломана)
            response_save_order.encoding = 'UTF-8'
            # Уже перекодированные данные выводим с помощью метода .text
            text_field_tab_2.insert(1.0, ('# ' + response_save_order.text + "\n" + "="*70 + "\n"))



    except OSError as e:
        #print(e)
        messagebox.showerror(title='Connection error', message=e)


def pay():
    xml_pay_string = '<RK7Query><RK7CMD CMD="PayOrder"><Order guid="' + str(entry_xml_create_tab_3_arg1.get()) +\
                     '"/><Cashier code="' + str(entry_xml_create_tab_3_arg2.get()) + '"/><Station code="'+  \
                     str(entry_xml_create_tab_3_arg3.get()) + '"/><Payment id="' + \
                     str(entry_xml_create_tab_3_arg4.get()) + '" amount="' + str(entry_xml_create_tab_3_arg5.get())\
                     + '"/></RK7CMD></RK7Query>'
    i_3 = ip_add_3.get()
    # i_2 = '172.22.3.86'
    p_3 = port_3.get()
    # p_2='4545'

    ip_string_3 = 'https://' + i_3 + ":" + p_3 + '/rk7api/v0/xmlinterface.xml'
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response_pay_order = session.request(method='POST', url=ip_string_3, data=xml_pay_string,auth=('admin', '1')
                                             , verify=False)
        xmldoc = minidom.parseString(response_pay_order.text)
        xmldoc.normalize()
        response_pay_order.encoding = 'UTF-8'
        text_field_tab_3.insert(1.0, ('# ' + response_pay_order.text + "\n" + "-" * 70 + "\n"))


    except OSError as e:
        #print(e)
        messagebox.showerror(title='Connection error', message=e)

'''Строим root окно'''

root = Tk()

root.iconbitmap(r'images\7.ico')
root.title("XML Parser v.1.2")

root.geometry("800x600+580+300")
# root.bind('<Return>', lambda e: request())
root.bind('<Escape>', lambda e: root.destroy())


'''Объявляем переменные'''

xml_arg1 = StringVar()
xml_arg2 = StringVar()
xml_arg3 = StringVar()
xml_arg4 = StringVar()
xml_arg5 = StringVar()

xml_arg1_tab_2 = StringVar()
xml_arg2_tab_2 = StringVar()
xml_arg3_tab_2 = StringVar()
xml_arg4_tab_2 = StringVar()
xml_arg5_tab_2 = StringVar()

xml_arg1_tab_3 = StringVar()
xml_arg2_tab_3 = StringVar()
xml_arg3_tab_3 = StringVar()
xml_arg4_tab_3 = StringVar()
xml_arg5_tab_3 = StringVar()

ip_add = StringVar()
port = StringVar()

ip_add_2 = StringVar()
port_2 = StringVar()

ip_add_3 = StringVar()
port_3 = StringVar()

tab_1 = ttk.Notebook(root, height=500, width=755)

tab_1.place(x=15, y=15)

'''Создаем frames для вкладок'''

frame_1 = ttk.Frame(tab_1)
frame_2 = ttk.Frame(tab_1)
frame_3 = ttk.Frame(tab_1)

tab_1.add(frame_1, text="Парсер")
tab_1.add(frame_2, text="Создание заказа")
tab_1.add(frame_3, text="Оплата заказа")


'''Первая вкладка'''

ip_label = Label(frame_1, text='IP-Address').place(x=25, y=8)
port_label = Label(frame_1, text='Port').place(x=115, y=8)
ip_address_entry = ttk.Entry(frame_1, width=20, textvariable=ip_add).place(x=15, y=30, width=90)
port_entry = ttk.Entry(frame_1, width=20, textvariable=port).place(x=110, y=30, width=40)


# entry_xml_request_arg1 = ttk.Entry(frame_1, width=20, textvariable=xml_arg1).place(x=15, y=70)
entry_xml_request_arg1 = ttk.Combobox(frame_1, values=['GetOrderList', 'GetWaiterList','GetRefList'], width=17, state='readonly')
entry_xml_request_arg1.place(x=15, y=70)
entry_xml_request_arg2 = ttk.Entry(frame_1, width=20, textvariable=xml_arg2).place(x=15, y=110)
entry_xml_request_arg3 = ttk.Entry(frame_1, width=20, textvariable=xml_arg3).place(x=15, y=150)
entry_xml_request_arg4 = ttk.Entry(frame_1, width=20, textvariable=xml_arg4).place(x=15, y=190)
entry_xml_request_arg5 = ttk.Entry(frame_1, width=20, textvariable=xml_arg5).place(x=15, y=230)

text_field = Text(frame_1, height=25, width=70, wrap=WORD, relief=SOLID)
text_field.place(x=170, y=70)

button_request = ttk.Button(frame_1, text='Request', command=request).place(x=15, y=270)

scrollbar = ttk.Scrollbar(frame_1, orient=VERTICAL, command=text_field.yview)
scrollbar.pack(side=RIGHT, fill=Y)
text_field.config(yscrollcommand=scrollbar.set)


'''Вторая вкладка'''
# Тип заказа
entry_xml_create_tab_2_arg1 = ttk.Entry(frame_2, width=20, textvariable=xml_arg1_tab_2)
entry_xml_create_tab_2_arg1.place(x=15, y=90)
label_xml_create_tab_2_arg1 = Label(frame_2, text='Тип заказа').place(x=15, y=68)
# Стол
entry_xml_create_tab_2_arg2 = ttk.Entry(frame_2, width=20, textvariable=xml_arg2_tab_2)
entry_xml_create_tab_2_arg2 .place(x=15, y=132)
label_xml_create_tab_2_arg2 = Label(frame_2, text='Стол').place(x=15, y=111)
# Код станции
entry_xml_create_tab_2_arg3 = ttk.Entry(frame_2, width=20, textvariable=xml_arg3_tab_2)
entry_xml_create_tab_2_arg3 .place(x=15, y=174)
label_xml_create_tab_2_arg3 = Label(frame_2, text='Код станции').place(x=15, y=153)
# Код блюда
entry_xml_create_tab_2_arg4 = ttk.Entry(frame_2, width=20, textvariable=xml_arg4_tab_2)
entry_xml_create_tab_2_arg4.place(x=15, y=216)
label_xml_create_tab_2_arg4 = Label(frame_2, text='Код блюда').place(x=15, y=195)
# Количество блюда
entry_xml_create_tab_2_arg5 = ttk.Entry(frame_2, width=20, textvariable=xml_arg5_tab_2)
entry_xml_create_tab_2_arg5.place(x=15, y=259)
label_xml_create_tab_2_arg5 = Label(frame_2, text='Количество блюд').place(x=15, y=237)

ip_label_tab_2 = Label(frame_2, text='IP-Address').place(x=25, y=8)
port_label_tab_2 = Label(frame_2, text='Port').place(x=115, y=8)

ip_address_entry_tab_2 = ttk.Entry(frame_2, width=20, textvariable=ip_add_2).place(x=15, y=30, width=90)
port_entry_tab_2 = ttk.Entry(frame_2, width=20, textvariable=port_2).place(x=110, y=30, width=40)

# Поле текста 2
text_field_tab_2 = Text(frame_2, height=25, width=70, wrap=WORD, relief=SOLID)
text_field_tab_2.place(x=170, y=70)

button_create = ttk.Button(frame_2, text='Создать', command=create).place(x=15, y=290)

scrollbar_tab_2 = ttk.Scrollbar(frame_2, orient=VERTICAL, command=text_field_tab_2.yview)
scrollbar_tab_2.pack(side=RIGHT, fill=Y)

# Добавим обратную связь - скроллбар будет анализировать количество текста и исходя из него отображать размер
text_field_tab_2.config(yscrollcommand=scrollbar_tab_2.set)


'''Третья вкладка'''

# GUID заказа
entry_xml_create_tab_3_arg1 = ttk.Entry(frame_3, width=20, textvariable=xml_arg1_tab_2)
entry_xml_create_tab_3_arg1.place(x=15, y=90)
label_xml_create_tab_3_arg1 = Label(frame_3, text='GUID заказа').place(x=15, y=68)
# Код кассира
entry_xml_create_tab_3_arg2 = ttk.Entry(frame_3, width=20, textvariable=xml_arg2_tab_2)
entry_xml_create_tab_3_arg2 .place(x=15, y=132)
label_xml_create_tab_3_arg2 = Label(frame_3, text='Код кассира').place(x=15, y=111)
# Код станции
entry_xml_create_tab_3_arg3 = ttk.Entry(frame_3, width=20, textvariable=xml_arg3_tab_2)
entry_xml_create_tab_3_arg3 .place(x=15, y=174)
label_xml_create_tab_3_arg3 = Label(frame_3, text='Код станции').place(x=15, y=153)
# ID валюты
entry_xml_create_tab_3_arg4 = ttk.Entry(frame_3, width=20, textvariable=xml_arg4_tab_2)
entry_xml_create_tab_3_arg4.place(x=15, y=216)
label_xml_create_tab_3_arg4 = Label(frame_3, text='ID валюты').place(x=15, y=195)
# Сумма
entry_xml_create_tab_3_arg5 = ttk.Entry(frame_3, width=20, textvariable=xml_arg5_tab_2)
entry_xml_create_tab_3_arg5.place(x=15, y=259)
label_xml_create_tab_3_arg5 = Label(frame_3, text='Сумма').place(x=15, y=237)

ip_address_entry_tab_3 = ttk.Entry(frame_3, width=20, textvariable=ip_add_3).place(x=15, y=30, width=90)
port_entry_tab_3 = ttk.Entry(frame_3, width=20, textvariable=port_3).place(x=110, y=30, width=40)

# Поле текста 3
text_field_tab_3 = Text(frame_3, height=25, width=70, wrap=WORD, relief=SOLID)
text_field_tab_3.place(x=170, y=70)

ip_label_tab_3 = Label(frame_3, text='IP-Address').place(x=25, y=8)
port_label_tab_3 = Label(frame_3, text='Port').place(x=115, y=8)

button_pay = ttk.Button(frame_3, text='Оплатить', command=pay).place(x=15, y=290)

scrollbar_tab_3 = ttk.Scrollbar(frame_3, orient=VERTICAL, command=text_field_tab_3.yview)
scrollbar_tab_3.pack(side=RIGHT, fill=Y)

# Добавим обратную связь - скроллбар будет анализировать количество текста и исходя из него отображать размер
text_field_tab_3.config(yscrollcommand=scrollbar_tab_3.set)
root.mainloop()
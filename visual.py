from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json
from xml.dom import minidom

class Visual:
    def __init__(self, root):
        self.root = root
        root.title("XML Parser v.1.3.0")
        root.iconbitmap(r'images\7.ico')

        '''Зададим размер и положение экрана в зависимости от размера экрана пользователя'''
        #root.geometry("900x700+500+600")
        w = 800  # width for the Tk root
        h = 600  # height for the Tk root

        # get screen width and height
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.bind('<Escape>', lambda e: root.destroy())

        # Используем установку сессий для keep-alive подключений вместо единомоментных выззовов (Use session for keep-alive
        # connections).
        session = requests.session()

        def open_file():
            try:
                file_path = filedialog.askopenfilename(title = "Choose your file", filetypes = [("json files","*.json")])
                l_ist = str(ip_add.get())
                # filename = 'presets.json'
                with open(file_path, 'r') as f_obj:
                    numbers = json.load(f_obj)
            except:
                pass

        def save_file():
            try:
                file_path = filedialog.asksaveasfilename(title = "Choose your file", filetypes = [("json files","*.json")])
                l_ist = str(ip_add.get())
                with open(file_path, 'r+') as f_obj:
                    json.dump(l_ist, f_obj)
            except:
                pass

        def request():
            # Получаем аргументы запроса
            # a1 = xml_arg1.get()
            a1 = self.entry_xml_request_arg1.get()
            a2 = xml_arg2.get()
            a3 = xml_arg3.get()
            a4 = xml_arg4.get()
            a5 = xml_arg5.get()

            i = ip_add.get()
            p = port.get()
            ''' Проверим, ввел ли ли пользователь ip и порт, если нет - выдадим ошибку'''
            if not i and not p:
                messagebox.showwarning(title='Error', message="Введите IP-адрес и порт!")

            else:
                '''Собираем строку запроса'''
                # Основное тело запроса
                xml_request_string = '<?xml version="1.0" encoding="UTF-8"?><RK7Query> <RK7CMD CMD="' + str(
                    a1) + '" /></RK7Query>'
                ip_string = 'https://' + i + ":" + p + '/rk7api/v0/xmlinterface.xml'

                try:
                    # Убираем warnings об SSL (warnings выводятся даже при отключении SSL)
                    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

                    # Старый запрос без поддержки keep-alive
                    # response = requests.get(ip_string, data=a, auth=('admin', '1'),verify=False)
                    # Запрос с выключенным SSL
                    response = session.request(method='GET', url=ip_string, data=xml_request_string, auth=('admin', '1'),
                                               verify=False)

                    xmldoc = minidom.parseString(response.text)
                    xmldoc.normalize()

                    if a1 == "GetOrderList":
                        i = 1
                        y = 1
                        # Обратимся к тегу Order
                        self.text_field.delete(1.0, END)
                        orders = xmldoc.getElementsByTagName("Order")
                        # Обратимся к тегу Visit
                        visits = xmldoc.getElementsByTagName("Visit")
                        for visit in visits:
                            self.text_field.insert(1.0, (
                            str(i) + ". " + "Визит (ID) = " + visit.attributes.item(0).value + "\n" + "Завершен"
                                                                                                      " = " + visit.attributes.item(
                                2).value + "\n" "Количество гостей = " + visit.attributes.item(3).value + "\n"
                            + "-" * 47 + "\n"))
                            i = i + 1
                        for order in orders:
                            self.text_field.insert(1.0, (str(y) + ". " + "Имя заказа = " + order.attributes.item(1).value + "\n"
                                                    + "GUID = " + order.attributes.item(
                                5).value + "\n" "Стол (ID) = " + order.attributes.item(6).value + "\n"
                                                    + "Стол (Код) = " + order.attributes.item(
                                7).value + "\n" + "Категория Заказа (ID) = " + order.attributes.
                                                    item(
                                8).value + "\n" + "Категория заказа (Код) = " + order.attributes.item(
                                9).value + "\n" + "Тип Заказа (ID)"
                                                  " = " + order.attributes.item(
                                10).value + "\n" + "Тип Заказа(Код) = " + order.attributes.item(11).value +
                                                    "\n" + "Официант (ID) = " + order.attributes.item(
                                12).value + "\n" + "Официант (код) = " + order.attributes
                                                    .item(13).value + "\n" + "Сумма заказа = " + order.attributes.item(
                                14).value + "\n" + "Сумма к оплате = "
                                                    + order.attributes.item(
                                15).value + "\n" + "PriceListSum = " + order.attributes.item(16).value + "\n" +
                                                    "Всего блюд = " + order.attributes.item(
                                17).value + "\n" + "Завершен = " + order.attributes.item(18).value
                                                    + "\n" + "Счет = " + order.attributes.item(
                                19).value + "\n" + "Открыт = " + order.attributes.item(20).value
                                                    + "\n" + "-" * 47 + "\n"))
                            y = y + 1


                    elif a1 == "GetWaiterList":
                        self.text_field.delete(1.0, END)
                        waiters = xmldoc.getElementsByTagName("waiter")
                        for waiter in waiters:
                            self.text_field.insert(1.0, (
                            "Официант (ID) = " + waiter.attributes.item(0).value + "\n" + "Официант (Код)= " +
                            waiter.attributes.item(1).value + "\n" + "-" * 47 + "\n"))

                    elif a1 == "GetRefList":
                        self.text_field.delete(1.0, END)
                        references = xmldoc.getElementsByTagName("RK7Reference")
                        for reference in references:
                            self.text_field.insert(1.0, (
                            "RefName = " + reference.attributes.item(0).value + " " + "Count = " + reference.
                            attributes.item(1).value + " " + "DataVersion = " + reference.attributes.item(
                                2).value + "\n" + "-" * 60 + "\n"))

                    else:
                        self.text_field.delete(1.0, END)
                        self.text_field.insert(1.0, response.content)

                except OSError as e:
                    print(e)
                    messagebox.showerror(title='Connection error', message=e)

                    # return(soup)

        def create():
            xml_request_string = '<?xml version="1.0" encoding="UTF-8"?><RK7Query><RK7CMD CMD="CreateOrder"><Order><OrderType' \
                                 ' code= "' + str(self.entry_xml_create_tab_2_arg1.get()) + '" /><Table code= "' + \
                                 str(self.entry_xml_create_tab_2_arg2.get()) + '" /></Order></RK7CMD></RK7Query>'
            i_2 = ip_add_2.get()
            # i_2 = '172.22.3.86'
            p_2 = port_2.get()
            # p_2='4545'
            ''' Проверим, ввел ли ли пользователь ip и порт, если нет - выдадим ошибку'''
            if not i_2 and not p_2:
                messagebox.showwarning(title='Error', message="Введите IP-адрес и порт!")

            else:
                ip_string_2 = 'https://' + i_2 + ":" + p_2 + '/rk7api/v0/xmlinterface.xml'
                try:
                    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                    response_create_order = session.request(method='POST', url=ip_string_2, data=xml_request_string,
                                                            auth=('admin', '1'), verify=False)
                    # response_2 = requests.post(ip_string_2, data=xml_request_string, auth=('admin', '1'),verify=False)
                    # print(response_create_order.content)
                    xmldoc = minidom.parseString(response_create_order.text)
                    xmldoc.normalize()
                    visitid = xmldoc.getElementsByTagName("RK7QueryResult")
                    for visit in visitid:
                        visit = visit.attributes.item(5).value
                        xml_save_order = '<RK7Query><RK7CMD CMD="SaveOrder" deferred="1" dontcheckLicense="1"><Order visit="' + \
                                         str(visit) + '" orderIdent="256" /><Session><Station code="' + \
                                         str(self.entry_xml_create_tab_2_arg3.get()) + '" /><Dish code="' + \
                                         str(self.entry_xml_create_tab_2_arg4.get()) + '" quantity="' + \
                                         str(self.entry_xml_create_tab_2_arg4.get()) + '"></Dish></Session></RK7CMD></RK7Query>'

                        xml_save_order_string = xml_save_order.encode('utf-8')
                        response_save_order = session.request(method='POST', url=ip_string_2, data=xml_save_order_string,
                                                              auth=('admin', '1'), verify=False)
                        # Перекодируем response_save_order в нужную нам кодировку (кириллица поломана)
                        response_save_order.encoding = 'UTF-8'
                        # Уже перекодированные данные выводим с помощью метода .text
                        self.text_field_tab_2.insert(1.0, ('# ' + response_save_order.text + "\n" + "=" * 70 + "\n"))



                except OSError as e:
                    # print(e)
                    messagebox.showerror(title='Connection error', message=e)

        def pay():
            xml_pay_string = '<RK7Query><RK7CMD CMD="PayOrder"><Order guid="' + str(self.entry_xml_create_tab_3_arg1.get()) + \
                             '"/><Cashier code="' + str(self.entry_xml_create_tab_3_arg2.get()) + '"/><Station code="' + \
                             str(self.entry_xml_create_tab_3_arg3.get()) + '"/><Payment id="' + \
                             str(self.entry_xml_create_tab_3_arg4.get()) + '" amount="' + str(
                self.entry_xml_create_tab_3_arg5.get()) \
                             + '"/></RK7CMD></RK7Query>'
            i_3 = ip_add_3.get()
            # i_2 = '172.22.3.86'
            p_3 = port_3.get()
            # p_2='4545'
            ''' Проверим, ввел ли ли пользователь ip и порт, если нет - выдадим ошибку'''
            if not i_3 and not p_3:
                messagebox.showwarning(title='Error', message="Введите IP-адрес и порт!")

            else:
                ip_string_3 = 'https://' + i_3 + ":" + p_3 + '/rk7api/v0/xmlinterface.xml'
                try:
                    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                    response_pay_order = session.request(method='POST', url=ip_string_3, data=xml_pay_string,
                                                         auth=('admin', '1')
                                                         , verify=False)
                    xmldoc = minidom.parseString(response_pay_order.text)
                    xmldoc.normalize()
                    response_pay_order.encoding = 'UTF-8'
                    self.text_field_tab_3.insert(1.0, ('# ' + response_pay_order.text + "\n" + "-" * 70 + "\n"))


                except OSError as e:
                    # print(e)
                    messagebox.showerror(title='Connection error', message=e)


        '''Объявили переменные для полей'''

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
        ip_add_2 = StringVar()
        ip_add_3 = StringVar()

        port = StringVar()
        port_2 = StringVar()
        port_3 = StringVar()

        '''Создали строку меню'''

        # Выключили старый стиль меню
        root.option_add('*tearOff', False)
        self.menubar = Menu(root)
        root.configure(menu=self.menubar)
        self.file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.file, label='File')
        self.file.add_command(label='Open...', command=open_file)
        self.file.add_command(label='Save', command=save_file)
        self.file.add_command(label='Exit', command=self.root.quit)

        '''Создали вкладки'''

        self.tab_1 = ttk.Notebook(root, height=500, width=755)
        self.tab_1.place(x=15, y=15)

        '''Создали frame'''

        self.frame_1 = ttk.Frame(self.tab_1)
        self.frame_2 = ttk.Frame(self.tab_1)
        self.frame_3 = ttk.Frame(self.tab_1)

        '''Добавили frame на вкладки и задали имена вкладок'''

        self.tab_1.add(self.frame_1, text="Парсер")
        self.tab_1.add(self.frame_2, text="Создание заказа")
        self.tab_1.add(self.frame_3, text="Оплата заказа")



        '''Первая вкладка'''



        self.entry_xml_request_arg1 = ttk.Combobox(self.frame_1, values=['GetOrderList', 'GetWaiterList', 'GetRefList']
                                                   , width=17, state='readonly')
        self.entry_xml_request_arg1.place(x=15, y=70)
        self.entry_xml_request_arg2 = ttk.Entry(self.frame_1, width=20, textvariable=xml_arg2).place(x=15, y=110)
        self.entry_xml_request_arg3 = ttk.Entry(self.frame_1, width=20, textvariable=xml_arg3).place(x=15, y=150)
        self.entry_xml_request_arg4 = ttk.Entry(self.frame_1, width=20, textvariable=xml_arg4).place(x=15, y=190)
        self.entry_xml_request_arg5 = ttk.Entry(self.frame_1, width=20, textvariable=xml_arg5).place(x=15, y=230)

        self.ip_label = Label(self.frame_1, text='IP-Address').place(x=25, y=8)
        self.port_label = Label(self.frame_1, text='Port').place(x=115, y=8)
        self.ip_address_entry = ttk.Entry(self.frame_1, width=20, textvariable=ip_add).place(x=15, y=30, width=90)
        self.port_entry = ttk.Entry(self.frame_1, width=20, textvariable=port).place(x=110, y=30, width=40)


        self.text_field = Text(self.frame_1, height=25, width=70, wrap=WORD, relief=SOLID)
        self.text_field.place(x=170, y=70)

        self.button_request = ttk.Button(self.frame_1, text='Request', command=request).place(x=15, y=270)

        self.scrollbar = ttk.Scrollbar(self.frame_1, orient=VERTICAL, command=self.text_field.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.text_field.config(yscrollcommand=self.scrollbar.set)



        '''Вторая вкладка'''


        # Тип заказа
        self.entry_xml_create_tab_2_arg1 = ttk.Entry(self.frame_2, width=20, textvariable=xml_arg1_tab_2)
        self.entry_xml_create_tab_2_arg1.place(x=15, y=90)
        self.label_xml_create_tab_2_arg1 = Label(self.frame_2, text='Тип заказа').place(x=15, y=68)
        # Стол
        self.entry_xml_create_tab_2_arg2 = ttk.Entry(self.frame_2, width=20, textvariable=xml_arg2_tab_2)
        self.entry_xml_create_tab_2_arg2.place(x=15, y=132)
        self.label_xml_create_tab_2_arg2 = Label(self.frame_2, text='Стол').place(x=15, y=111)
        # Код станции
        self.entry_xml_create_tab_2_arg3 = ttk.Entry(self.frame_2, width=20, textvariable=xml_arg3_tab_2)
        self.entry_xml_create_tab_2_arg3.place(x=15, y=174)
        self.label_xml_create_tab_2_arg3 = Label(self.frame_2, text='Код станции').place(x=15, y=153)
        # Код блюда
        self.entry_xml_create_tab_2_arg4 = ttk.Entry(self.frame_2, width=20, textvariable=xml_arg4_tab_2)
        self.entry_xml_create_tab_2_arg4.place(x=15, y=216)
        self.label_xml_create_tab_2_arg4 = Label(self.frame_2, text='Код блюда').place(x=15, y=195)
        # Количество блюда
        self.entry_xml_create_tab_2_arg5 = ttk.Entry(self.frame_2, width=20, textvariable=xml_arg5_tab_2)
        self.entry_xml_create_tab_2_arg5.place(x=15, y=259)
        self.label_xml_create_tab_2_arg5 = Label(self.frame_2, text='Количество блюд').place(x=15, y=237)

        self.ip_label_tab_2 = Label(self.frame_2, text='IP-Address').place(x=25, y=8)
        self.port_label_tab_2 = Label(self.frame_2, text='Port').place(x=115, y=8)

        self.ip_address_entry_tab_2 = ttk.Entry(self.frame_2, width=20, textvariable=ip_add_2).place(x=15, y=30, width=90)
        self.port_entry_tab_2 = ttk.Entry(self.frame_2, width=20, textvariable=port_2).place(x=110, y=30, width=40)

        # Поле текста 2
        self.text_field_tab_2 = Text(self.frame_2, height=25, width=70, wrap=WORD, relief=SOLID)
        self.text_field_tab_2.place(x=170, y=70)

        self.button_create = ttk.Button(self.frame_2, text='Создать', command=create).place(x=15, y=290)

        self.scrollbar_tab_2 = ttk.Scrollbar(self.frame_2, orient=VERTICAL, command=self.text_field_tab_2.yview)
        self.scrollbar_tab_2.pack(side=RIGHT, fill=Y)

        # Добавим обратную связь - скроллбар будет анализировать количество текста и исходя из него отображать размер
        self.text_field_tab_2.config(yscrollcommand=self.scrollbar_tab_2.set)

        '''Третья вкладка'''

        # GUID заказа
        self.entry_xml_create_tab_3_arg1 = ttk.Entry(self.frame_3, width=20, textvariable=xml_arg1_tab_2)
        self.entry_xml_create_tab_3_arg1.place(x=15, y=90)
        self.label_xml_create_tab_3_arg1 = Label(self.frame_3, text='GUID заказа').place(x=15, y=68)
        # Код кассира
        self.entry_xml_create_tab_3_arg2 = ttk.Entry(self.frame_3, width=20, textvariable=xml_arg2_tab_2)
        self.entry_xml_create_tab_3_arg2.place(x=15, y=132)
        self.label_xml_create_tab_3_arg2 = Label(self.frame_3, text='Код кассира').place(x=15, y=111)
        # Код станции
        self.entry_xml_create_tab_3_arg3 = ttk.Entry(self.frame_3, width=20, textvariable=xml_arg3_tab_2)
        self.entry_xml_create_tab_3_arg3.place(x=15, y=174)
        self.label_xml_create_tab_3_arg3 = Label(self.frame_3, text='Код станции').place(x=15, y=153)
        # ID валюты
        self.entry_xml_create_tab_3_arg4 = ttk.Entry(self.frame_3, width=20, textvariable=xml_arg4_tab_2)
        self.entry_xml_create_tab_3_arg4.place(x=15, y=216)
        self.label_xml_create_tab_3_arg4 = Label(self.frame_3, text='ID валюты').place(x=15, y=195)
        # Сумма
        self.entry_xml_create_tab_3_arg5 = ttk.Entry(self.frame_3, width=20, textvariable=xml_arg5_tab_2)
        self.entry_xml_create_tab_3_arg5.place(x=15, y=259)
        self.label_xml_create_tab_3_arg5 = Label(self.frame_3, text='Сумма').place(x=15, y=237)

        self.ip_address_entry_tab_3 = ttk.Entry(self.frame_3, width=20, textvariable=ip_add_3).place(x=15, y=30, width=90)
        self.port_entry_tab_3 = ttk.Entry(self.frame_3, width=20, textvariable=port_3).place(x=110, y=30, width=40)

        # Поле текста 3
        self.text_field_tab_3 = Text(self.frame_3, height=25, width=70, wrap=WORD, relief=SOLID)
        self.text_field_tab_3.place(x=170, y=70)

        self.ip_label_tab_3 = Label(self.frame_3, text='IP-Address').place(x=25, y=8)
        self.port_label_tab_3 = Label(self.frame_3, text='Port').place(x=115, y=8)

        self.button_pay = ttk.Button(self.frame_3, text='Оплатить', command=pay).place(x=15, y=290)

        self.scrollbar_tab_3 = ttk.Scrollbar(self.frame_3, orient=VERTICAL, command=self.text_field_tab_3.yview)
        self.scrollbar_tab_3.pack(side=RIGHT, fill=Y)

        # Добавим обратную связь - скроллбар будет анализировать количество текста и исходя из него отображать размер
        self.text_field_tab_3.config(yscrollcommand=self.scrollbar_tab_3.set)


root = Tk()
visual = Visual(root)

root.mainloop()
def collections_call:
	try:
		попытка подключния к серверу
		попытка ввода авторизационных данных
	except:
		сервер не доступен
	except:
		данные не верные
	else:
		выполняем команду запроса референтных данных
		
class Stress_functions:
    def start_testing:
		try:
			попытка подключния к серверу
			попытка ввода авторизационных данных
		except:
			сервер не доступен
		except:
			данные не верные
		else:
			начало выполнения процедуры тестирования
				try:
					создание заказа
					try:
						оплата заказа
					except:
						обработка ошибки
					else:
						выполнение процедуры оплаты
				except:
					обработка ошибки
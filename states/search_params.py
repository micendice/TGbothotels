from telebot.handler_backends import State, StatesGroup


class SearchParamState(StatesGroup):
    city = State()
    hotels_num = State()
    need_photo = State()
    num_photo = State()
    calendar_checkin = State()
    calendar_checkout = State()
    complete = State()
    menu = State()
    cust_param = State()
    guests_num = State()



""" После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)
"""
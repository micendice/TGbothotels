from loader import bot
from states.search_params import SearchParamState
from telebot.types import Message
from keyboards.reply.y_or_no import y_or_no


@bot.message_handler(commands=["highprice"])
def highprice(message: Message):
    bot.set_state(message.from_user.id, SearchParamState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name} \n'
                                           f'Введите город для поиска отелей. ')


@bot.message_handler(state=SearchParamState.city)
def get_city(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Спасибо, записал. Сколько отелей вывести? (не больше пяти, пожалуйста)")
        bot.set_state(message.from_user.id, SearchParamState.hotels_num, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, "Название города может содержать только буквы латинского алфавита")


@bot.message_handler(state=SearchParamState.hotels_num)
def get_city(message: Message) -> None:
    if message.text.isdigit() and int(message.text) <= 5:
        bot.send_message(message.from_user.id, "Спасибо, записал. "
                                               "Нужно ли показывать фотографии отелей? Нажмите 'Да' или 'Нет'",
                         reply_markup=y_or_no("Нужно ли показывать фотографии отелей? "))
        bot.set_state(message.from_user.id, SearchParamState.need_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_num'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, "Для ввода количества показываемых отелей введите число от 1 до 5")


@bot.message_handler(state=SearchParamState.need_photo)
def get_need_photo(message: Message) -> None:
    if message.text == 'ДА':
        bot.send_message(message.from_user.id, "Спасибо, записал. Сколько фотографий показывать?(не больше четырех, пожалуйста)")
        bot.set_state(message.from_user.id, SearchParamState.num_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = True
            print("Need Photo parameter", data["need_photo"])
    elif message.text == 'НЕТ':
        bot.send_message(message.from_user.id, "Спасибо, записал. Вопросов больше не имею)")
        bot.set_state(message.from_user.id, SearchParamState.complete, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = False
            data['num_photo'] = 0
    print("Need Photo parameter", data["need_photo"])


@bot.message_handler(state=SearchParamState.num_photo)
def get_num_photo(message: Message) -> None:
    if message.text.isdigit() and int(message.text) <= 4:
        bot.send_message(message.from_user.id, "Спасибо, записал. Вопросов больше не имею)")
        bot.set_state(message.from_user.id, SearchParamState.complete, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['num_photo'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, "Для ввода количества показываемых фотографий введите число от 1 до 5")


@bot.message_handler(state=SearchParamState.complete)
def params_ready(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        text = f"Ищем самые дорогие гостиницы по следующим параметрам\nГород: {data['city']} \n" \
               f"Показать {data['hotels_num']} отелей" \
                f"\nПоказывать {data['num_photo']} фото \n"
        bot.send_message(message.from_user.id, text)


""" После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)
  city = State()
    hotels_num = State()
    need_photo = State()
    num_photo = State()
    количество отелей, необходимость показа фото и их количество\n'
                                           f'В ответ получите список отелей с самой высокой ценой
    
"""

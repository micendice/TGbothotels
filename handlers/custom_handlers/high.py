
from loader import bot
from states.search_params import SearchParamState
from telebot.types import Message
from keyboards.reply.y_or_no import y_or_no
from typing import Dict
from config_data.config import CITY_TEMPLATE, MAX_PHOTO_DISPLAYED, MAX_HOTEL_DISPLAYED
import re

city_pattern = CITY_TEMPLATE
max_photo = MAX_PHOTO_DISPLAYED
max_hotel = MAX_HOTEL_DISPLAYED


def final_text(message: Message, data: Dict):

    text = f"Ищем самые дорогие гостиницы по следующим параметрам\nГород: {data['city']} \n" \
            f"Показать {data['hotels_num']} отеля" \
            f"\nПоказывать {data['num_photo']} фото"

    bot.send_message(message.from_user.id, text, reply_markup=y_or_no(f"Всё верно?\n "
                                                                        f"ДА - начать поиск\n "
                                                                        f"НЕТ - ввести параметры заново"))


@bot.message_handler(commands=["highprice"])
def highprice(message: Message):
    bot.set_state(message.from_user.id, SearchParamState.city, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name} \n'
                                           f'Введите город для поиска отелей. ')


@bot.message_handler(state=SearchParamState.city)
def get_city(message: Message) -> None:
    if re.match(city_pattern, message.text):      # regexp here .  pattern imported from config
        bot.send_message(message.from_user.id, f"Спасибо, записал. Сколько отелей вывести? "
                                               f"(не больше {max_hotel}, пожалуйста)")
        bot.set_state(message.from_user.id, SearchParamState.hotels_num, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
    else:
        bot.send_message(message.from_user.id, "Название города может содержать только "
                                               "буквы латинского алфавита, пробелы и тире")


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
        bot.send_message(message.from_user.id, f"Для ввода количества показываемых отелей "
                                               f"введите число от 1 до {max_hotel}")


@bot.message_handler(state=SearchParamState.need_photo)
def get_need_photo(message: Message) -> None:
    if message.text == 'ДА':
        bot.send_message(message.from_user.id, f"Спасибо, записал. Сколько фотографий показывать?"
                                               f"(не больше {max_photo}, пожалуйста)")
        bot.set_state(message.from_user.id, SearchParamState.num_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = True

    elif message.text == 'НЕТ':
        bot.send_message(message.from_user.id, "Спасибо, записал. Итак, проверьте, пожалуйста, все ли верно:")
        bot.set_state(message.from_user.id, SearchParamState.complete, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = False
            data['num_photo'] = 0
            final_text(message, data)
    else:
        bot.send_message(message.from_user.id, "Нужно ли показывать фотографии отелей?\n"
                                               " Пожалуйста, ответьте ДА или НЕТ",
                         reply_markup=y_or_no("Нужно ли показывать фотографии отелей? "))


@bot.message_handler(state=SearchParamState.num_photo)
def get_num_photo(message: Message) -> None:
    if message.text.isdigit() and 0 < int(message.text) <= 4:
        bot.send_message(message.from_user.id, "Спасибо, записал. Итак, проверьте, пожалуйста, все ли верно:")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            bot.set_state(message.from_user.id, SearchParamState.complete, message.chat.id)
            data['num_photo'] = int(message.text)
            final_text(message, data)
    else:
        bot.send_message(message.from_user.id, "Для ввода количества показываемых фотографий "
                                               "введите число от 1 до {max_photo}")


@bot.message_handler(state=SearchParamState.complete)
def params_ready(message: Message) -> None:
    if message.text == 'ДА':
        pass
    elif message.text == 'НЕТ':
        bot.set_state(message.from_user.id, SearchParamState.city, message.chat.id)
        bot.send_message(message.from_user.id, f'Хммм... Хорошо, {message.from_user.first_name}, попробуем еще раз.\n'
                                               f'Введите город для поиска отелей. ')
    else:
        bot.send_message(message.from_user.id, "Пожалуйста, ответьте ДА или НЕТ")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            final_text(message, data)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data)


""" После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)
"""

from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loader import bot
from states.search_params import SearchParamState
from telebot.types import Message, InputMediaPhoto

from keyboards.reply.y_or_no import y_or_no
from keyboards.inline.custom_keyb import custom_reply_markup

from typing import Dict
from config_data.config import CITY_TEMPLATE, MAX_PHOTO_DISPLAYED, MAX_HOTEL_DISPLAYED, SEARCH_INTERVAL, MAX_STAY, \
    payload_hotels_list, payload_summary, payload_get_offer, command_set, sort_params

import re
import datetime
from site_API.utils.site_api_handler import site_api
from database.core import crud
from database.common.models import History, db

import logging

today = datetime.date.today()

db_write = crud.create()
db_read = crud.retrieve()

logger_1 = logging.getLogger(__name__)
logger_1.setLevel(logging.INFO)

handler_1 = logging.FileHandler(f"{__name__}.log", mode="w")
formatter_1 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler_1.setFormatter(formatter_1)
logger_1.addHandler(handler_1)

logger_1.info(f"Core working now")


def final_text(data: Dict):
    text = f"Ищем {command_set[data['command_name']]['russ_word']} по следующим параметрам\n" \
           f"Город: {data['city']} \n" \
           f"Показать {data['hotels_num']} отеля" \
           f"\nПоказывать {data['num_photo']} фото" \
           f"\nДаты проживания: c {data['checkin']} по {data['checkout']}" \
           f"\nВсё верно?\n" \
           f"ДА - начать поиск\n" \
           f"НЕТ - ввести параметры заново"

    return text


def write_db(data: Dict) -> None:

    data_to_write = [{
        "command": data["command_name"],
        "pl_sort": data["sorting_pl"],
        "city": data["city"],
        "hotels_num": data["hotels_num"],
        "num_photo": data["num_photo"] if data["need_photo"] else "No Photo",
        "check_in_date": data["checkin"],
        "check_out_date": data["checkout"],
        "full_result": data["hotels_list"],
        "result_descr": [data["hotels_list"][hotel_id]["result_descr"] for hotel_id in data["hotels_list"].keys()]
    }]
    db_write(db, History, data_to_write)


def read_db():
    col_to_read = (
        "created_at",
        "command",
        "pl_sort",
        "city",
        "hotels_num",
        "num_photo",
        "check_in_date",
        "check_out_date",
        "result_descr"
    )
    result_db_read = db_read(db, History, col_to_read)
    print(result_db_read)
    return result_db_read


def start_calendar(message: Message, calendar_id: str, start_date, final_date):
    calendar, step = DetailedTelegramCalendar(calendar_id=calendar_id, min_date=start_date,
                                              max_date=final_date, locale="ru").build()

    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)
    return start_date

"""
@bot.message_handler(commands=["highprice"])
def highprice(message: Message) -> None:
    bot.set_state(message.from_user.id, SearchParamState.city, message.chat.id)
    bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name} \n"
                                            f"Введите город для поиска отелей. ")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command_name"] = "highprice"
        data["sorting_pl"] = sort_params["sort_high"]"""


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith("sort_"))
def custom_sort_btn_handler(c):
    bot.set_state(c.message.chat.id, SearchParamState.city, c.message.chat.id)
    with bot.retrieve_data(c.from_user.id) as data:
        data["sorting_pl"] = sort_params[c.data]
    bot.send_message(c.message.chat.id, f"Введите город для поиска отелей. ")


@bot.message_handler(state=SearchParamState.city)
def get_city(message: Message) -> None:
    if re.match(CITY_TEMPLATE, message.text):      # regexp here .  pattern imported from config
        location = site_api.find_location(message.text.lower())

        if location:                    # checking site database - if the location exist
            bot.send_message(message.from_user.id, f"Спасибо, записал. Сколько отелей вывести? "
                                               f"(не больше {MAX_HOTEL_DISPLAYED}, пожалуйста)")
            bot.set_state(message.from_user.id, SearchParamState.hotels_num, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data["city"] = message.text.lower()
                data["regionId"] = location

        else:
            print("Google haven't found such place. Город не найден")

    else:
        bot.send_message(message.from_user.id, "Название города может содержать только "
                                               "буквы латинского алфавита, пробелы и тире")


@bot.message_handler(state=SearchParamState.hotels_num)
def hotels_num(message: Message) -> None:
    if message.text.isdigit() and int(message.text) <= MAX_HOTEL_DISPLAYED:
        bot.send_message(message.from_user.id, "Спасибо, записал. "
                                               "Нужно ли показывать фотографии отелей? Нажмите 'Да' или 'Нет'",
                         reply_markup=y_or_no("Нужно ли показывать фотографии отелей? "))
        bot.set_state(message.from_user.id, SearchParamState.need_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["hotels_num"] = int(message.text)
    else:
        bot.send_message(message.from_user.id, f"Для ввода количества показываемых отелей "
                                               f"введите число от 1 до {MAX_HOTEL_DISPLAYED}")


@bot.message_handler(state=SearchParamState.need_photo)
def get_need_photo(message: Message) -> None:
    if message.text == "ДА":
        bot.send_message(message.from_user.id, f"Спасибо, записал. Сколько фотографий показывать?"
                                               f"(не больше {MAX_PHOTO_DISPLAYED}, пожалуйста)")
        bot.set_state(message.from_user.id, SearchParamState.num_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["need_photo"] = True

    elif message.text == 'НЕТ':
        bot.send_message(message.from_user.id, "Спасибо, записал. Осталось выбрать даты проживания."
                                               " Введите дату заезда")
        bot.set_state(message.from_user.id, SearchParamState.calendar_checkin, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = False
            data['num_photo'] = 0
        start_date = today
        final_date = datetime.timedelta(days=SEARCH_INTERVAL) + start_date
        return start_calendar(message, 'checkin', start_date, final_date)               #запуск календаря

    else:
        bot.send_message(message.from_user.id, "Нужно ли показывать фотографии отелей?\n"
                                               " Пожалуйста, ответьте ДА или НЕТ",
                         reply_markup=y_or_no("Нужно ли показывать фотографии отелей? "))


@bot.message_handler(state=SearchParamState.num_photo)
def get_num_photo(message: Message) -> None:
    if message.text.isdigit() and 0 < int(message.text) <= MAX_PHOTO_DISPLAYED:
        bot.send_message(message.from_user.id, "Спасибо, записал. Осталось выбрать даты проживания. "
                                               "Введите дату заезда")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            bot.set_state(message.from_user.id, SearchParamState.calendar_checkin, message.chat.id)
            data["num_photo"] = int(message.text)
            start_date = today
            final_date = datetime.timedelta(days=SEARCH_INTERVAL) + start_date
            return start_calendar(message, "checkin", start_date, final_date)               # Запуск календаря
    else:
        bot.send_message(message.from_user.id, f"Для ввода количества показываемых фотографий "
                                               f"введите число от 1 до {MAX_PHOTO_DISPLAYED}")


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id="checkin"))
def calendar_callback_in(c, calendar_id: str = 'checkin', start_date=today):
    final_date = datetime.timedelta(days=SEARCH_INTERVAL) + start_date

    result, key, step = DetailedTelegramCalendar(calendar_id=calendar_id, min_date=start_date, max_date=final_date,
                                                 locale="ru").process(c.data)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result} \nТеперь выберите дату выезда",
                              c.message.chat.id,
                              c.message.message_id)

        with bot.retrieve_data(c.from_user.id) as data:
            data[calendar_id] = result

            start_date = result
            final_date = datetime.timedelta(days=MAX_STAY) + start_date
            return start_calendar(c.message, 'checkout', start_date, final_date)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id="checkout"))
def calendar_callback_out(c, calendar_id: str = "checkout"):
    with bot.retrieve_data(c.from_user.id) as data:
        start_date = data["checkin"]
        final_date = datetime.timedelta(days=MAX_STAY) + start_date

        result, key, step = DetailedTelegramCalendar(calendar_id=calendar_id, min_date=start_date, max_date=final_date,
                                                     locale="ru").process(c.data)
        if not result and key:
            bot.edit_message_text(f"Выберите {LSTEP[step]}",
                                  c.message.chat.id,
                                  c.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"Вы выбрали {result} ",
                                  c.message.chat.id,
                                  c.message.message_id)
            data[calendar_id] = result
            bot.set_state(c.message.chat.id, SearchParamState.complete, c.message.chat.id)
            text = final_text(data)
            bot.send_message(c.message.chat.id, text, reply_markup=y_or_no(f"Всё верно?\n "
                                                                              f"ДА - начать поиск\n "
                                                                              f"НЕТ - ввести параметры заново"))


@bot.message_handler(state=SearchParamState.complete)
def params_ready(message: Message) -> None:

    if message.text == "ДА":
        pass

    elif message.text == "НЕТ":
        bot.set_state(message.from_user.id, SearchParamState.city, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data.clear()                       #starting from the very beginning. Changing state and clearing data dict
        bot.send_message(message.from_user.id, f"Хммм... Хорошо, {message.from_user.first_name}, попробуем еще раз.\n"
                                               f"Введите город для поиска отелей. ")
    else:
        bot.send_message(message.from_user.id, "Пожалуйста, ответьте ДА или НЕТ")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            text = final_text(data)
            bot.send_message(message.from_user.id, text, reply_markup=y_or_no(f"Всё верно?\n "
                                                                              f"ДА - начать поиск\n "
                                                                              f"НЕТ - ввести параметры заново"))

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        payload_hotels_list["destination"]["regionId"] = data["regionId"]
        payload_hotels_list["checkInDate"]["day"] = data["checkin"].day
        payload_hotels_list["checkInDate"]["month"] = data["checkin"].month
        payload_hotels_list["checkInDate"]["year"] = data["checkin"].year
        payload_hotels_list["checkOutDate"]["day"] = data["checkout"].day
        payload_hotels_list["checkOutDate"]["month"] = data["checkout"].month
        payload_hotels_list["checkOutDate"]["year"] = data["checkout"].year

        payload_hotels_list["resultsSize"] = data["hotels_num"]
        payload_hotels_list["sort"] = data["sorting_pl"]
        payload_hotels_list["filters"] = command_set[data['command_name']]['filters_command']

        data["checkInDate"] = payload_hotels_list["checkInDate"]
        data["checkOutDate"] = payload_hotels_list["checkOutDate"]

        data["hotels_list"] = site_api.get_hotels_list(payload_hotels_list)

        payload_get_offer["checkInDate"] = data["checkInDate"]
        payload_get_offer["checkOutDate"] = data["checkOutDate"]
        payload_get_offer["destination"]["regionId"] = data["regionId"]
        num_photo = data["num_photo"]

        for hotel_id in data["hotels_list"].keys():
            payload_summary["propertyId"] = hotel_id
            payload_get_offer["propertyId"] = hotel_id

            #print(payload_get_offer, "*"*20)

            hotel_summary_dict = site_api.get_hotel_summary(payload=payload_summary, num_photo=num_photo)
            hotel_price = site_api.get_hotel_price(payload_get_offer)

            data["hotels_list"][hotel_id]["short_descr"] = hotel_summary_dict["short_descr"]
            data["hotels_list"][hotel_id]["addressline"] = hotel_summary_dict["addressline"]
            data["hotels_list"][hotel_id]["accomodation_price"] = hotel_price
            if data["need_photo"]:
                data["hotels_list"][hotel_id]["photo_urls"] = hotel_summary_dict["urlphoto"]

        logger_1.info(f"data")

        for hotel_id, hotel_info in data["hotels_list"].items():            #sending messages with hotels info

            text = f"{hotel_info['name']}\n{hotel_info['addressline']}\n{hotel_info['short_descr']}" \
                   f"\nPrice: {hotel_info['accomodation_price']} "
            data["hotels_list"][hotel_id]["result_descr"] = text

            if "photo_urls" in hotel_info.keys():
                photo_urls_list: list = hotel_info["photo_urls"]

                media_group = list()        #creating media pack for each hotel
                num = 0
                for photo_url in photo_urls_list:
                    media_group.append(InputMediaPhoto(photo_url, caption=text if num == 0 else ''))
                    num += 1
                bot.send_media_group(message.from_user.id, media=media_group)

            else:
                bot.send_message(message.from_user.id, text)

        write_db(data)
        data.clear()
    bot.set_state(message.from_user.id, SearchParamState.menu, message.chat.id)
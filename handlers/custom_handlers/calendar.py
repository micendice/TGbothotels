from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loader import bot
import datetime
from telebot.types import Message
from config_data.config import SEARCH_INTERVAL


def start_calendar(message: Message, calendar_id: str, start_date, final_date):
    calendar, step = DetailedTelegramCalendar(calendar_id=calendar_id, min_date=start_date,
                                              max_date=final_date, locale="ru").build()
                                              #
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


"""@bot.callback_query_handler(func=DetailedTelegramCalendar.func())"""


def calendar_callback(c, calendar_id: str, start_date: datetime.date):
    final_date = datetime.timedelta(days=SEARCH_INTERVAL) + start_date

    result, key, step = DetailedTelegramCalendar(calendar_id=calendar_id, min_date=start_date, max_date=final_date,
                                                 locale="ru").process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)
        print(result)
        with bot.retrieve_data(c.from_user.id) as data:  # , c.chat.id

            data[calendar_id] = result
            print(data)



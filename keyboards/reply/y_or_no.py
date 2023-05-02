from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from loader import bot


"""def y_or_no(question:str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    yes_button = InlineKeyboardButton(text="Да", callback_data='yes')
    no_button = InlineKeyboardButton(text="Нет", callback_data='no')
    print("Задан вопрос: ", question)
    keyboard.add(yes_button, no_button)
    return keyboard


@bot.callback_quiery_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'yes':
        return True
    elif callback.data == 'no':
        return False
    """


def y_or_no(question: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton('ДА'), KeyboardButton('НЕТ'))
    print("Задан вопрос: ", question)
    return keyboard

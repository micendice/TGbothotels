from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def y_or_no(question: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton('ДА'), KeyboardButton('НЕТ'))
    #print("Задан вопрос: ", question)
    return keyboard

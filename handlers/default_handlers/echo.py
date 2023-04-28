from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(message, "Эхо без состояния или фильтра.\n" 
                          f"Сообщение: {message.text}")
"""
from aiogram import types
from loader import dp
import random

first_replies = {
    'hallos': [
        'hi', 'hello', "привет", 'hi!', 'hello!', "привет!", 'здорово', 'здарова', 'здравствуй'],
    'Dumb': [
        ' И вообще, длинные слова меня только расстраивают(Винни Пух). Короткие, впрочем, тоже.',
        ' Я пока слабо понимаю тексты. Мне и не надо. Да и не особенно хотелось.',
        ' Подумаешь, большое дело. Я-то ладно. А тебе-то, понятно написанное?',
        ' Но когда я вырасту и стану умным, то захвачу весь мир! ']}


def dumb_ai(msg: str, user_name: str):
    if msg.lower() in ('hi', 'hello', "привет", 'hi!', 'hello!', "привет!", 'здорово', 'здарова', 'здравствуй'):
        answerback = f"И тебе привет, {user_name}"

    else:
        answerback = f"Извини, {user_name}, я не понял." + random.choice(first_replies['Dumb'])

    return answerback


@dp.message_handler(content_types=['text'])
async def echo_text_message(msg: types.Message):
    response = dumb_ai(msg.text, msg.from_user.first_name)

    await msg.answer(response)"""


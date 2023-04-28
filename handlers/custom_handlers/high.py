from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message
"""
from aiogram import types
from loader import dp


@dp.message_handler(commands=['highprice'])
async def high_command(message: types.Message):
    await message.reply("Введите город, количество отелей, необходимость показа фото и их количество\n"
                        "В ответ получите список отелей с самой высокой ценой")

"""

@bot.message_handler(command=["highprice"])
def highprice(message: Message):
    #bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет {message.from_user.username} \n'
                                           f'Введите город, количество отелей, необходимость показа фото и их количество\n'
                                           f'В ответ получите список отелей с самой высокой ценой')


""" После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
3. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)
"""

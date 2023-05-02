"""from aiogram import types
from loader import dp


@dp.message_handler(commands=['history'])
async def history_command(message: types.Message):
    await message.reply("Здесь будет функция предоставления информации об истории запросов.\n "
                        "Строка 2")"""
from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message


@bot.message_handler(commands=["history"])
def history(message: Message):
    #bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет {message.from_user.username} \n'
                                           f'После ввода команды пользователю выводится история поиска отелей\n'
                                           f'Line 2')

"""После ввода команды пользователю выводится история поиска отелей. Сама история
содержит:
1. Команду, которую вводил пользователь.
2. Дату и время ввода команды.
3. Отели, которые были найдены."""

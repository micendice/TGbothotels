from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message
"""
from aiogram import types
from loader import dp

@dp.message_handler(commands=['bestdeal'])
async def custom_command(message: types.Message):
    await message.reply("Введите город, диапазон цен, расстояние до центра, количество показываемых отелей, необходимость показа фото и их количество\n"
                        "В ответ получите информацию об отелях")
                        """


@bot.message_handler(command=["bestdeal"])
def bestdeal(message: Message):
    #bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет {message.from_user.username} \n'
                                           f'Bestdeal command\n'
                                           f'Line2')

"""После ввода команды у пользователя запрашивается:
1. Город, где будет проводиться поиск.
2. Диапазон цен.
3. Диапазон расстояния, на котором находится отель от центра.
4. Количество отелей, которые необходимо вывести в результате (не больше
заранее определённого максимума).
5. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
a. При положительном ответе пользователь также вводит количество
необходимых фотографий (не больше заранее определённого
максимума)"""
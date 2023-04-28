from aiogram import types
from loader import dp


@dp.message_handler(commands=['history'])
async def history_command(message: types.Message):
    await message.reply("Здесь будет функция предоставления информации об истории запросов.\n "
                        "Строка 2")


"""После ввода команды пользователю выводится история поиска отелей. Сама история
содержит:
1. Команду, которую вводил пользователь.
2. Дату и время ввода команды.
3. Отели, которые были найдены."""

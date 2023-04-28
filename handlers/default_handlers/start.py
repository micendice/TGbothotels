from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.reply_to(message, f'Привет, {message.from_user.full_name}!\n'
                          f'Я - бот, предоставляющий информацию об отелях.\n '
                    f'Будут реализованы команды бота:\n '
                    f' /highprice\n '
                    f' /lowprice\n '
                    f' /bestdeal\n '
                    f' /history\n')


"""
from aiogram import types
from loader import dp

@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.reply(f'Здравствуй, {msg.from_user.first_name}. Я - бот, предоставляющий информацию об отелях.\n '
                    f'Будут реализованы команды бота:\n '
                    f' /highprice\n '
                    f' /lowprice\n '
                    f' /bestdeal\n '
                    f' /history\n')
"""


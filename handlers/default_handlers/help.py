"""from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot
@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))"""

from aiogram import types
from loader import dp


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Здесь будет подсказка по работе с ботом.\n "
                        "Строка подсказки 2")
    print('Help command requested!')

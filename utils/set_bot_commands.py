"""from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )
"""

from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS
from loader import bot


async def setup_default_bot_commands():

    await bot.set_my_commands(DEFAULT_COMMANDS)


async def setup_custom_bot_commands():

    await bot.set_my_commands(CUSTOM_COMMANDS)



"""
if __name__ ==  '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)"""
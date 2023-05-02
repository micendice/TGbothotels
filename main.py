from loader import bot
import handlers  # noqa
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands, set_custom_commands

f"""rom aiogram import executor
from loader import dp


from handlers.default_handlers.start import start_command
from handlers.default_handlers.help import help_command
from handlers.custom_handlers.high import high_command
from handlers.custom_handlers.low import low_command
from handlers.custom_handlers.custom import custom_command
from handlers.custom_handlers.history import history_command
from handlers.default_handlers.echo import echo_text_message


start_command
help_command
high_command
low_command
custom_command
history_command
echo_text_message
"""


if __name__ == "__main__":
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    set_custom_commands(bot)
    bot.infinity_polling()
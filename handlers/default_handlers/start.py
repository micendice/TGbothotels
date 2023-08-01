from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.reply_to(message, f'Привет, {message.from_user.full_name}!\n'
                          f'Я - бот, предоставляющий информацию об отелях.\n '
                    f'Доступны следующие команды:\n '
                    f' /highprice - Поиск самых дорогих отелей\n По'
                    f' /lowprice - Поиск самых дешевых отелей\n '
                    f' /bestdeal - Поиск отелей по критерию\n '
                    f' /history - Вывод последних 10 запросов')



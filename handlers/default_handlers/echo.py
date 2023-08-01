from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(message, f"Если вы это видите, то скорее всего, вы просто набрали что-то не то. "
                          f"Следуйте моим подсказкам и все будет хорошо. Вы справитесь, это несложно.")
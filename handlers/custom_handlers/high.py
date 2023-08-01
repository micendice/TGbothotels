
import logging

from loader import bot
from telebot.types import Message
from states.search_params import SearchParamState

from config_data.config import sort_params
from database.core import crud


db_write = crud.create()
db_read = crud.retrieve()

logger_1 = logging.getLogger(__name__)
logger_1.setLevel(logging.INFO)

handler_1 = logging.FileHandler(f"{__name__}.log", mode="a", encoding="utf-8")
formatter_1 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler_1.setFormatter(formatter_1)
logger_1.addHandler(handler_1)

logger_1.info(f"Testing logging from the very beginning")


@bot.message_handler(commands=["highprice"])
def highprice(message: Message) -> None:
    logger_1.info(f"highprice command started")
    bot.set_state(message.from_user.id, SearchParamState.city, message.chat.id)
    bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name} \n"
                                            f"Введите город для поиска отелей. ")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["user_id"] = str(message.from_user.id)
        data["command_name"] = "highprice"
        data["sorting_pl"] = sort_params["sort_high"]


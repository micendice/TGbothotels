
import logging

from loader import bot
from telebot.types import Message

from database.core import crud
from database.common.models import History, db
from . core import write_db

db_write = crud.create()
db_read = crud.retrieve()


logger_3 = logging.getLogger(__name__)
logger_3.setLevel(logging.DEBUG)

handler_3 = logging.FileHandler(f"{__name__}.log", mode="a")
formatter_3 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler_3.setFormatter(formatter_3)
logger_3.addHandler(handler_3)

logger_3.debug(f"history command")


def read_db(current_user_id):
    result_db_read = db_read(db, History).where(History.user_id == current_user_id).limit(10).order_by(History.id.desc())
    db_recs = result_db_read.dicts().execute()
    logger_3.info(f"Reading db")
    return db_recs


@bot.message_handler(commands=["history"])
def history(message: Message) -> None:
    current_user_id = str(message.from_user.id)
    text_to_report = str()
    for i_dict in read_db(current_user_id):
        #logger_3.debug(f"Record , {record}")
        line = f"Номер записи: {i_dict['id']}, User ID: {i_dict['user_id']} , время создания: {i_dict['created_at']}, " \
            f"команда: {i_dict['command']}, город: {i_dict['city']} \n"
        text_to_report += line

    data_to_fill = {
        "user_id": str(message.from_user.id),
        "command_name": "history",
        "sorting_pl": "n/a",
        "city": "n/a",
        "hotels_num": "n/a",
        "need_photo": "n/a",
        "num_photo": "n/a",
        "rooms_payload": [{"adults": "n/a", "children": []}],     #emty list means 0 instead of n/a in db
        "checkin": "n/a",
        "checkout": "n/a",
        "hotels_list": {"1": {"result_descr": "n/a"}},
    }
    write_db(data_to_fill)

    bot.send_message(message.from_user.id,
                     f"О, {message.from_user.first_name}! \n"
                     f"Спешу исполнить твою команду\n"
                     f"Узри же историю последних десяти запросов!\n {text_to_report}")
    logger_3.info(f"history command completed")


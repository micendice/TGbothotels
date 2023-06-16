
import logging

from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message
from database.core import crud
from database.common.models import History, db
#from . core import read_db
db_write = crud.create()
db_read = crud.retrieve()


logger_3 = logging.getLogger(__name__)
logger_3.setLevel(logging.DEBUG)

handler_3 = logging.FileHandler(f"{__name__}.log", mode="w")
formatter_3 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler_3.setFormatter(formatter_3)
logger_3.addHandler(handler_3)

logger_3.debug(f"Testing logging in debugging process")


def read_db():

    result_db_read = db_read(db, History).limit(10).order_by(History.id.desc())

    db_recs = result_db_read.dicts().execute()
    for record in db_recs:
        print('Record ', record)

    return db_recs


@bot.message_handler(commands=["history"])
def history(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     f"О, {message.from_user.first_name}! \n"
                     f"Спешу исполнить твою команду\n"
                     f"Узри же историю последних десяти запросов!" )
    text_bd = read_db()

    logger_3.debug(f"Trying to write down data into db:")



    bot.send_message(message.from_user.id,
                     f"О, {message.from_user.first_name}! \n"
                     f"Спешу исполнить твою команду\n"
                     f"Узри же историю последних десяти запросов!")

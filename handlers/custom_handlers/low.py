
from loader import bot
from telebot.types import Message
from states.search_params import SearchParamState
from config_data.config import sort_params


@bot.message_handler(commands=["lowprice"])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, SearchParamState.city, message.chat.id)
    bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name} \n"
                                           f"Введите город для поиска отелей. ")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["user_id"] = str(message.from_user.id)

        data["command_name"] = "lowprice"
        data["sorting_pl"] = sort_params["sort_low"]
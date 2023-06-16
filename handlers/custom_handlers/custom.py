from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message
from keyboards.inline.custom_keyb import custom_reply_markup
from states.search_params import SearchParamState


@bot.message_handler(commands=["custom"])
def custom(message: Message) -> None:
    bot.set_state(message.from_user.id, SearchParamState.cust_param, message.chat.id)
    bot.send_message(message.from_user.id, f"Привет {message.from_user.first_name} \n"
                                           f"Вы выбрали команду поиска отелей по критерию\n"
                                           f"Доступны следующие критерии: \n"
                                           f"1. Лучшие по цене и отобранные hotels.com \n"
                                           f"2. С самым высоким рейтингом гостей \n"
                                           f"3. Ближайшие к центру города \n"
                                           f"4. По количеству звезд \n"
                                           f"5. Самые рекомендуемые ", reply_markup=custom_reply_markup)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["command_name"] = "custom"

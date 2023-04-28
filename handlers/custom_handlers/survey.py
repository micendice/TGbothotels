from keyboards.reply.contact import request_contact
from loader import bot
from states.contact_info import UserInfoState
from telebot.types import Message



@bot.message_handler(commands=["survey"])
def survey(message:Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}введи свое имя')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Спасибо, записал. Теперь введи свой возраст")
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text
    else:
        bot.send_message(message.from_user.id, "Имя может содержать только буквы")


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Спасибо, записал. Теперь введи свою страну")
        bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text
    else:
        bot.send_message(message.from_user.id, "Возраст выражается числом")


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.from_user.id, "Спасибо, записал. Теперь введи свой город")
        bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['country'] = message.text
    else:
        bot.send_message(message.from_user.id, "Страна пишется буквами")


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, "Спасибо, записал. Отправь свой номер нажав на кнопку",
                     reply_markup=request_contact())
    bot.set_state(message.from_user.id, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@bot.message_handler(content_types=['text', 'contact'], state=UserInfoState.phone_number)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            text = f"Ай, молодца! Все предоставил. Твои данные:\n" \
                   f"Имя - {data['name']}\n" \
                   f"Возраст - {data['age']}\n" \
                   f"Страна - {data['country']}\n" \
                   f"Город - {data['city']}\n" \
                   f"Номер телефона - {data['phone_number']}\n"
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, "Чтобы отправить контакт, нажми на кнопку")

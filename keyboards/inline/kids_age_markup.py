from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


kids_age_btns = [
    InlineKeyboardButton("До 1 года", callback_data="age_0"),
    InlineKeyboardButton("1 год", callback_data="age_1"),
    InlineKeyboardButton("2 года", callback_data="age_2"),
    InlineKeyboardButton("3 года", callback_data="age_3"),
    InlineKeyboardButton("4 года", callback_data="age_4"),
    InlineKeyboardButton("5 лет", callback_data="age_5"),
    InlineKeyboardButton("6 лет", callback_data="age_6"),
    InlineKeyboardButton("7 лет", callback_data="age_7"),
    InlineKeyboardButton("8 лет", callback_data="age_8"),
    InlineKeyboardButton("9 лет", callback_data="age_9"),
    InlineKeyboardButton("10 лет", callback_data="age_10"),
    InlineKeyboardButton("11 лет", callback_data="age_11"),
    InlineKeyboardButton("12 лет", callback_data="age_12"),
    InlineKeyboardButton("13 лет", callback_data="age_13"),
    InlineKeyboardButton("14 лет", callback_data="age_14"),
    InlineKeyboardButton("15 лет", callback_data="age_15"),
    InlineKeyboardButton("16 лет", callback_data="age_16"),
    InlineKeyboardButton("17 лет", callback_data="age_17")
]
# сборка клавиатуры из кнопок `InlineKeyboardButton`

kids_age_markup = InlineKeyboardMarkup(build_menu(kids_age_btns, n_cols=4))


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


adults_num_list = [
    InlineKeyboardButton("1 взрослый", callback_data="adults_1"),
    InlineKeyboardButton("2 взрослых", callback_data="adults_2"),
    InlineKeyboardButton("3 взрослых", callback_data="adults_3"),
    InlineKeyboardButton("4 взрослых", callback_data="adults_4")
]


kids_num_list = [
    InlineKeyboardButton("Без детей (лучший вариант отдыха)", callback_data="kids_0"),
    InlineKeyboardButton("1 ребенок", callback_data="kids_1"),
    InlineKeyboardButton("2 ребенка", callback_data="kids_2"),
    InlineKeyboardButton("3 ребенка", callback_data="kids_3"),
    InlineKeyboardButton("4 ребенка", callback_data="kids_4")
]
# сборка клавиатуры из кнопок `InlineKeyboardButton`
adults_reply_markup = InlineKeyboardMarkup(build_menu(adults_num_list, n_cols=1))
kids_reply_markup = InlineKeyboardMarkup(build_menu(kids_num_list, n_cols=1))



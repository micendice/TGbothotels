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


button_list = [
    InlineKeyboardButton("1. Цена и релевантность", callback_data="sort_price_rel"),
    InlineKeyboardButton("2. Отзывы гостей", callback_data="sort_guest_rating"),
    InlineKeyboardButton("3. Ближайшие к центру города", callback_data="sort_distance_from_dt"),
    InlineKeyboardButton("4. Звездность отеля", callback_data="sort_stars"),
    InlineKeyboardButton("5. Рекомендованные", callback_data="sort_recommended")
]

# сборка клавиатуры из кнопок `InlineKeyboardButton`
custom_reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))



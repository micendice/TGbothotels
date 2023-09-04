from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from handlers.custom_handlers.core import location_list


def build_menu(buttons, n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


# building up list of buttons
virtual_locations = []
for i_loc in location_list:
    displayed_value = i_loc["display_name"]
    cb_data = "location_" + str(i_loc["gaiaId"])

    virtual_locations.append(InlineKeyboardButton(displayed_value, callback_data=cb_data))


# сборка клавиатуры из кнопок `InlineKeyboardButton`
location_choice_markup = InlineKeyboardMarkup(build_menu(virtual_locations, n_cols=1))


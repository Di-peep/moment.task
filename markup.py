from telebot import types


def hide_markup():
    markup = types.ReplyKeyboardRemove()
    return markup


def gen_sex_markup():
    markup = types.InlineKeyboardMarkup()
    male = types.InlineKeyboardButton(text='🚹', callback_data='1')
    female = types.InlineKeyboardButton(text='🚺', callback_data='0')
    markup.row(male, female)
    return markup


def main_menu_markup():
    menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    menu_markup.row('Інформація про мене')
    menu_markup.row('Налаштування')
    return menu_markup


def settings_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Змінити ім'я")
    markup.row("Змінити вік")
    markup.row("Змінити стать")
    markup.row("Назад")
    return markup


def change_name_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # markup.row("Змінити ім'я")
    markup.row("Назад")
    return markup


def change_age_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # markup.row("Так, змінити вік")
    markup.row("Назад")
    return markup


def change_sex_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Змінити стать")
    markup.row("Назад")
    return markup

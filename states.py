from markup import *
from validator import *
from object_bot import bot


# відповідь на всі НЕ реплайнові повідомлення
text_error = 'Якщо щось потрібно - використовуйте кнопки.'
invalid_data = 'Введені невалідні дані.\nСпробуйте ще раз.'


def main_menu(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            "Головне меню:",
            reply_markup=main_menu_markup()
            )
    else:
        if message.text == 'Інформація про мене':
            try:
                chat_id = message.chat.id
                bot.send_message(chat_id, f"<i>Інформація про користувача:</i>\n"
                                          f"<b>Ім'я:</b> {user.name}\n"
                                          f"<b>Вік:</b> {user.age}\n"
                                          f"<b>Стать:</b> {user.sex}",
                                 parse_mode='html')

            except Exception as e:
                print(e)
                bot.reply_to(message, "З вашими данними щось трапилось...")

        elif message.text == 'Налаштування':
            return True, 'settings'

        else:
            bot.send_message(message.chat.id, text_error)

    return False, ''


def settings(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            "Меню налаштувань:",
            reply_markup=settings_markup()
            )
    else:
        if message.text == "Змінити ім'я":
            return True, 'change_name'

        elif message.text == 'Змінити вік':
            return True, 'change_age'

        elif message.text == 'Змінити стать':
            return True, 'change_sex'

        elif message.text == 'Назад':
            return True, 'main_menu'

        else:
            bot.send_message(message.chat.id, text_error)

    return False, ''


def change_name(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            "На яке бажаєте змінити ім'я?",
            reply_markup=change_name_markup()
            )
    else:
        if message.text == 'Назад':
            return True, 'settings'

        elif check_name(message.text):
            user.add_name(message.text)
            bot.send_message(message.chat.id,
                             f"Збережене нове ім'я: <i>{user.name}</i>",
                             parse_mode='html'
                             )
            return True, 'settings'

        else:
            bot.send_message(message.chat.id, invalid_data)

    return False, ''


def change_age(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            "На який бажаєте змінити вік?",
            reply_markup=change_age_markup()
            )
    else:
        if message.text == "Назад":
            return True, 'settings'

        elif check_age(message.text):
            user.add_age(message.text)
            bot.send_message(message.chat.id,
                             f"Збережене новий вік: <i>{user.age}</i>",
                             parse_mode='html'
                             )
            return True, 'settings'

        else:
            bot.send_message(message.chat.id, invalid_data)

    return False, ''


def change_sex(message, user, is_entry=False):
    if is_entry:
        bot.send_message(
            message.chat.id,
            f"Ваша стать - <i>{user.sex}</i>\nБажаєте змінити стать на протилежну?",
            reply_markup=change_sex_markup(),
            parse_mode='html'
            )
    else:
        if message.text == "Змінити стать":
            if user.sex == 'male':
                user.add_sex('female')

            elif user.sex == 'female':
                user.add_sex('male')

            bot.send_message(message.chat.id,
                             f"Стать змінено на протилежну!\nТепер ваша стать - <i>{user.sex}</i>",
                             parse_mode='html'
                             )

        elif message.text == 'Назад':
            return True, 'settings'

        else:
            bot.send_message(message.chat.id, text_error)

    return False, ''

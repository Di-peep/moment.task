from validator import check_name, check_age
from all_markup import *


# release
# token = ''

# test token
token = ''


bot = telebot.TeleBot(token)

users = {}  # ніяких бд не підключав, тому всі юзера будуть в оп зберігатись


class User:
    def __init__(self):
        self.name = None
        self.age = None
        self.sex = None
        self.step = 0

    def add_name(self, name):
        self.name = name

    def add_age(self, age):
        self.age = age

    def add_sex(self, sex):
        self.sex = sex


@bot.message_handler(commands=['start'])
def start_registration(message):
    chat_id = message.chat.id

    if chat_id in users:
        bot.send_message(chat_id, "Ви уже зареєстровані!", reply_markup=main_menu_markup())
    else:
        users[chat_id] = User()

        msg = bot.send_message(chat_id, "Введіть своє ім'я:")
        bot.register_next_step_handler(msg, reg_name)


def reg_name(message):
    chat_id = message.chat.id
    user = users[chat_id]

    if check_name(message.text):
        user.add_name(message.text)

        msg = bot.send_message(chat_id, "Який ваш вік?")
        bot.register_next_step_handler(msg, reg_age)
    else:
        msg = bot.reply_to(message, "Будь ласка, введіть коректне ім'я")
        bot.register_next_step_handler(msg, reg_name)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    user = users[chat_id]

    if call.message:
        choose_sex = {
            '1': 'male',
            '0': 'female'
        }

        response = choose_sex.get(call.data)
        user.add_sex(response)
        # bot.send_message(chat_id, 'Done!')
        bot.answer_callback_query(call.id, "Зарєстровано!")
        reg_end(chat_id)


def reg_age(message):
    chat_id = message.chat.id
    user = users[chat_id]

    if check_age(message.text):
        user.add_age(message.text)
        bot.send_message(chat_id, "Ваша стать?", reply_markup=gen_sex_markup())
    else:
        msg = bot.reply_to(message, "Будь ласка, введіть коректний вік:")
        bot.register_next_step_handler(msg, reg_age)


def reg_end(ch_id):
    try:
        chat_id = ch_id
        bot.send_message(chat_id, "Реєстрацію завершено!")

        bot.send_message(chat_id, "Дивіться меню:", reply_markup=main_menu_markup())

    except Exception as e:
        print(e)


def about(chat_id):
    try:
        bot.send_message(chat_id, f"<i>Інформація про користувача:</i>\n"
                                  f"<b>Ім'я:</b> {users[chat_id].name}\n"
                                  f"<b>Вік:</b> {users[chat_id].age}\n"
                                  f"<b>Стать:</b> {users[chat_id].sex}",
                                  parse_mode='html')

    except Exception as e:
        print(e)
        bot.send_message(chat_id, "З вашими данними щось трапилось...")


def settings(chat_id):
    # chat_id = message.chat.id
    bot.send_message(chat_id,  "Налаштування:", reply_markup=gen_settings_markup())

########################################################################################################################


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    chat_id = message.chat.id

    if message.text == 'Назад':
        if users[chat_id].step == 0:
            bot.send_message(chat_id, "Головне меню:", reply_markup=main_menu_markup())
        else:
            bot.send_message(chat_id, "Меню налаштувань:", reply_markup=gen_settings_markup())

    elif message.text == "Змінити ім'я":
        bot.send_message(chat_id, "Бажаєте змінити ім'я?", reply_markup=change_name_markup())

    elif message.text == 'Змінити вік':
        bot.send_message(chat_id, "Бажаєте змінити вік?", reply_markup=change_age_markup())

    elif message.text == 'Змінити стать':
        bot.send_message(chat_id, f"Ваша стать: {users[chat_id].sex}")
        msg = bot.send_message(chat_id, "Бажаєте змінити стать на протилежну?", reply_markup=change_sex_markup())
        bot.register_next_step_handler(msg, change_sex)

    elif message.text == "Так, змінити ім'я":
        hide_markup()
        msg = bot.send_message(chat_id, "Введіть нове ім'я:", reply_markup=hide_markup())
        bot.register_next_step_handler(msg, change_name)

    elif message.text == "Так, змінити вік":
        hide_markup()
        msg = bot.send_message(chat_id, "Введіть новий вік:", reply_markup=hide_markup())
        bot.register_next_step_handler(msg, change_age)

    elif message.text == 'Інформація про мене':
        about(chat_id)

    elif message.text == 'Налаштування':
        settings(chat_id)

    else:
        bot.send_message(chat_id, "Якщо щось потрібно - використовуйте кнопки")


def change_name(message):
    chat_id = message.chat.id
    user = users[chat_id]

    if message.text != 'Назад':
        if check_name(message.text):
            user.add_name(message.text)
            bot.send_message(chat_id, "Зареєстровано нове ім'я", reply_markup=gen_settings_markup())
        else:
            msg = bot.send_message(chat_id, "Введіть коректні дані")
            bot.register_next_step_handler(msg, change_name)
    else:
        bot.send_message(chat_id, "Меню налаштувань:", reply_markup=gen_settings_markup())


def change_age(message):
    chat_id = message.chat.id
    user = users[chat_id]

    if message.text != 'Назад':
        if check_age(message.text):
            user.add_age(message.text)
            bot.send_message(chat_id, "Зареєстровано новий вік", reply_markup=gen_settings_markup())
        else:
            msg = bot.send_message(chat_id, "Введіть коректні дані")
            bot.register_next_step_handler(msg, change_age)
    else:
        bot.send_message(chat_id, "Меню налаштувань:", reply_markup=gen_settings_markup())


def change_sex(message):
    chat_id = message.chat.id
    user = users[chat_id]

    if message.text != 'Назад':

        if user.sex == 'male':
            user.sex = 'female'

        elif user.sex == 'female':
            user.sex = 'male'

        bot.send_message(chat_id, "Стать змінено на протилежну!", reply_markup=gen_settings_markup())
    else:
        bot.send_message(chat_id, "Меню налаштувань:", reply_markup=gen_settings_markup())


bot.polling(none_stop=True)

# if __name__ == '__main__':
#      # bot.infinity_polling()
#      bot.polling(none_stop=True)

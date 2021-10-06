import telebot
from telebot import types
import time

token = ''

bot = telebot.TeleBot(token)

users = {}  # ніяких бд не підключав, тому всі юзера будуть в оп зберігатись


class User:
    def __init__(self):
        self.name = None
        self.age = None
        self.sex = None

    def add_name(self, name):
        self.name = name

    def add_age(self, age):
        self.age = age

    def add_sex(self, sex):
        self.sex = sex


def check_name(text):
    return text.isalpha() and 2 < len(text) < 20


def check_age(num):
    return num.isdigit() and 3 < int(num) < 100


@bot.message_handler(commands=['start'])
def start_registration(message):
    chat_id = message.chat.id
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


def gen_markup_sex():
    markup = types.InlineKeyboardMarkup()
    male = types.InlineKeyboardButton(text='🚹', callback_data='1')
    female = types.InlineKeyboardButton(text='🚺', callback_data='0')
    markup.row(male, female)
    return markup


def reg_age(message):
    chat_id = message.chat.id
    user = users[chat_id]

    if check_age(message.text):
        user.add_age(message.text)
        bot.send_message(chat_id, "Ваша стать?", reply_markup=gen_markup_sex())
    else:
        msg = bot.reply_to(message, "Будь ласка, введіть коректний вік:")
        bot.register_next_step_handler(msg, reg_age)


def main_menu_markup():
    menu_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    menu_markup.row('/about_me')
    menu_markup.row('/settings')
    return menu_markup


def reg_end(ch_id):
    try:
        chat_id = ch_id
        bot.send_message(chat_id, "Реєстрацію завершено!")

        time.sleep(1)  # спорно
        bot.send_message(chat_id, "Дивіться меню:", reply_markup=main_menu_markup())

    except Exception as e:
        print(e)


def hide_markup(chat_id):
    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "⌨💤...", reply_markup=markup)
    # return hide_markup


@bot.message_handler(commands=['about_me'])
def about(message):
    try:
        chat_id = message.chat.id
        bot.send_message(chat_id, f"<i>Інформація про користувача:</i>\n"
                                  f"<b>Ім'я:</b> {users[chat_id].name}\n"
                                  f"<b>Вік:</b> {users[chat_id].age}\n"
                                  f"<b>Стать:</b> {users[chat_id].sex}",
                                  parse_mode='html')

    except Exception as e:
        print(e)
        bot.reply_to(message, "З вашими данними щось трапилось...")


def gen_markup_settings():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Змінити ім'я")
    markup.row("Змінити вік")
    markup.row("Змінити стать")
    markup.row("Назад")
    return markup


@bot.message_handler(commands=['settings'])
def settings(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,  "Налаштування:", reply_markup=gen_markup_settings())

########################################################################################################################


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    chat_id = message.chat.id

    if message.text == "Змінити ім'я":
        hide_markup(chat_id)
        msg = bot.send_message(chat_id, "Введіть нове ім'я:")
        bot.register_next_step_handler(msg, change_name)

    elif message.text == 'Змінити вік':
        hide_markup(chat_id)
        msg = bot.send_message(chat_id, "Введіть новий вік:")
        bot.register_next_step_handler(msg, change_age)

    elif message.text == 'Змінити стать':
        if users[chat_id].sex:
            change_sex(chat_id)
            bot.send_message(chat_id, "Стать змінено!")
        else:
            bot.send_message(chat_id, "Стать ще не введена")

    elif message.text == 'Назад':
        bot.send_message(chat_id, "Головне меню:", reply_markup=main_menu_markup())
    else:
        bot.send_message(chat_id, "Якщо щось потрібно - використовуйте кнопки")


def change_name(message):
    chat_id = message.chat.id
    user = users[chat_id]

    if check_name(message.text):
        user.add_name(message.text)
        bot.send_message(chat_id, "Зареєстровано нове ім'я", reply_markup=gen_markup_settings())
    else:
        msg = bot.send_message(chat_id, "Введіть коректні дані")
        bot.register_next_step_handler(msg, change_name)


def change_age(message):
    chat_id = message.chat.id
    user = users[chat_id]

    if check_age(message.text):
        user.add_age(message.text)
        bot.send_message(chat_id, "Зареєстровано новий вік", reply_markup=gen_markup_settings())
    else:
        msg = bot.send_message(chat_id, "Введіть коректні дані")
        bot.register_next_step_handler(msg, change_age)


def change_sex(user_id):
    if users[user_id].sex == 'male':
        users[user_id].sex = 'female'

    elif users[user_id].sex == 'female':
        users[user_id].sex = 'male'


bot.polling(none_stop=True)

# if __name__ == '__main__':
#      # bot.infinity_polling()
#      bot.polling(none_stop=True)

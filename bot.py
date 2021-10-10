from validator import check_name, check_age

from markup import main_menu_markup, gen_sex_markup
from state_handler import get_state_and_process

from object_bot import bot
from object_user import User


# ніяких бд не підключав, тому всі юзера будуть в оп зберігатись
# всі кроки реєстрації залишив тут
# все решта повиносив

users = {}


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


@bot.message_handler(content_types=["text"])
def handle_message(message):
    try:
        chat_id = message.chat.id
        user = users[chat_id]

        get_state_and_process(message, user)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)


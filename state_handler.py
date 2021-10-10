from states import *
from object_user import User


states = {
    'main_menu': main_menu,
    'settings': settings,
    'change_name': change_name,
    'change_age': change_age,
    'change_sex': change_sex
}


def get_state_and_process(message, user: User, is_entry=False):
    if user.state in states:
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    else:
        user.state = 'choose_language_state'
        change_state, state_to_change_name = states[user.state](message, user, is_entry)
    if change_state:
        go_to_state(message, state_to_change_name, user)


def go_to_state(message, state_name: str, user: User):
    user.state = state_name
    get_state_and_process(message, user, is_entry=True)

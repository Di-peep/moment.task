def check_name(text):
    return text.isalpha() and 2 < len(text) < 20


def check_age(num):
    return num.isdigit() and 3 < int(num) < 100

class User:
    def __init__(self):
        self.name = None
        self.age = None
        self.sex = None
        self.state = 'main_menu'

    def add_name(self, name):
        self.name = name

    def add_age(self, age):
        self.age = age

    def add_sex(self, sex):
        self.sex = sex

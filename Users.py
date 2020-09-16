import csv

class User:
    online = True
    def __init__(self, username, password, balance):
         self.username = username
         self.password = password
         self.balance = balance

    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    def get_balance(self):
        return self.balance
    def is_register(self):
        f = open('users.txt', 'r')
        for line in f:
            users = line.split(":")
            if users[0] == self.get_username():
                return True
                f.close()
        f.close()
        return False
    def set_balance(self, coins):
        f = open('balances.txt', 'a')
        f.write(self.get_username() + ":" + int(coins) + '\n')
        f.close()
    def add_coins(self, coins):
        f = open('balances.txt', 'a')
        f.write(self.get_username() + ":" + int(get_balance(username) + coins) + '\n')
        f.close()

online = False
username = ''



def information_panel():
    print('start - Начать игру')
    print('job - список работ')

    choose = input()

    # if choose == 'start':
    #
    # elif choose == 'job':
    #     pass


def register_user():
    username = input("Введите логин: ")
    password = input("Введите пароль: ")
    user_1 = User(username, password, 0)

    if user_1.is_register() == True:
        print('Данный пользователь уже существует!')
        register_user()
        return

    f = open('users.txt', 'a')
    f.write(username + ":" + password + '\n')
    print('Вы успешно создали аккаунт!')
    information_panel(username)
    f.close()

def choose_login_and_registarion():
    if online == True:
        return
    choose = int(input("1 - регистрация; 2 - авторизация: "))
    if choose == 1:
        register_user()
    elif choose == 2:
        login_user()
    choose_login_and_registarion()

def get_balance(username):
    with open('sw_data.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['login'] == username:
                return row['balance']

def set_balance(username, coins):
    with open('sw_data.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['login'] != username:
                return

    with open('sw_data.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow(username.split(',') + password.split(',') + str(balance).split(','))

def add_coins(username, coins):
    f = open('balances.txt', 'a')
    coin = get_balance(username) + coins
    f.write(username + ":" + str(coin) + '\n')
    f.close()


def login_user():
    print("Для входа в аккаунт: ")
    username = input(" Введите логин: ")
    password = input(" Введите пароль: ")
    f = open('users.txt', 'r')

    for line in f:
        users = line.split(":")
        if password.lower() == (users[1].replace('\n', '')).lower() and users[0] == username:
           user_1 = User(username, password, get_balance(username))
           print('Вы успешно вошли в аккаунт!')
           information_panel(username)
           f.close()
           return

    print("Неправильный логин или пароль!")
    f.close()
    choose_login_and_registarion()

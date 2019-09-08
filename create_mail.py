# На вход подаються строки: Фамилия;Имя (пока из list.py)
from list import list_fio

import transliterate
import yandex_connect
import PASSWORDS
import string
import random
import re

# Токен Яндекса, действует год
token = PASSWORDS.logins['token_yandex']
# Единый пароль для всех создаваемых почт
mypassword = PASSWORDS.logins['default_ymail_password']

api = yandex_connect.YandexConnectDirectory(token, org_id=None)


# Посмотреть список групп
# department_list = api.department_list_full()
# print(department_list)
# {'id': 4, 'name': '@ДРУЗЬЯ_ШКОЛЫ'}

def randompassword():
    """Пароль для Zoom"""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # size = random.randint(8, 12) # Размер пароля всегда 10 символов
    size = 8
    password = ''.join(random.choice(chars) for x in range(size))
    # Заменить все буквы которые могут быть неправильно поняты пользователями
    for ch in ['l', 'j', 'i', '0', 'o', 'O']:
        if ch in password:
            password = password.replace(ch, random.choice(chars))
    # Пароль должен содержать хотя бы одну цифру (Zoom), если цифры нет, подставляем на треью позицию случайню цифру
    if not re.search(r'\d', password):
        password = password[:2] + random.choice(string.digits) + password[2 + 1:]
    # Два последних символа - два маленькие буквы, так удобнее потом дописывать 55
    password = password + random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
    return password


def create_fio_mail():
    for line in list_fio.splitlines():
        # Когда копирю из Google Sheets разделитель = Tab
        line = line.split('\t')
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        line.append((transliterate.translit(line[0], reversed=True).replace("'", "")
                     + "_"
                     + transliterate.translit(line[1], reversed=True)).replace("'", ""))
        print(line)
        create_mail(line[2], line[0], line[1])
        print(randompassword())


def create_famaly_mail():
    for line in list_fio.splitlines():
        # Когда копирю из Google Sheets разделитель = Tab
        line = line.split(' ')
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        line.append(transliterate.translit(line[0], reversed=True).replace("'", ""))
        print(line)
        password = randompassword()
        create_mail(line[2], line[0], line[1], password)
        print(password)


def create_mail(nickname_, secname_, name_, password_=mypassword):
    """
    Create Yandex mail.
    :param nickname: Login
    :param secname: Second Name
    :param name: First Name
    """
    try:
        # https://yandex.ru/dev/connect/directory/api/concepts/users/add-user-docpage/
        result = api.user_add(nickname=nickname_, password=password_, department_id=4, secname=secname_,
                              name=name_)
        print(result)
        print(result['email'])
    except yandex_connect.YandexConnectExceptionY as e:
        # print(e.args[0])
        if e.args[0] == 500:
            print(f"Unhandled exception: Такой пользователь уже существует: {nickname_ + '@givinschool.org'}")
        else:
            print("ERROR = " + e.__str__())
    # Вывести пароль в любом случае, т.к. он может пригодиться
    # print(password_)

if __name__ == "__main__":
    create_fio_mail()
    # create_famaly_mail()
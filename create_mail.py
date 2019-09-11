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


def randompassword(strong=False, long=8):
    """Генератор пароля для Zoom"""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    if strong:
        chars = chars + "@#$&"
    password = ''.join(random.choice(chars) for x in range(long))
    # Заменить все буквы которые могут быть неправильно поняты пользователями
    for ch in ['l', 'j', 'i', '0', 'o', 'O']:
        if ch in password:
            password = password.replace(ch, random.choice(chars))
    # Пароль должен содержать хотя бы одну цифру (Zoom), если цифры нет, подставляем на третью позицию случайню цифру
    if not re.search(r'\d', password):
        password = password[:2] + random.choice(string.digits) + password[2 + 1:]
    # В сложном пароле должны быть и спецсимволы, если нет, подставляем на третью позицию
    chars = set('@#$&', )
    if not any((c in chars) for c in password):
        password = password[:2] + random.choice(['@', '#', '$', '&']) + password[2 + 1:]
    # (Только для Zoom (strong=False)) Два последних символа - два маленькие буквы, так удобнее потом дописывать 55
    if not strong:
        password = password[:-2] + random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
    return password


def create_fio_mail():
    """ Русские Имя и Фамилия (для Друзей Школы)"""
    for line in list_fio.splitlines():
        # Когда копирю из Google Sheets разделитель = Tab
        # Бликс	Ирина
        line = line.split('\t')
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        line.append((transliterate.translit(line[0], reversed=True).replace("'", "")
                     + "_"
                     + transliterate.translit(line[1], reversed=True)).replace("'", ""))
        print(line)
        # ['Бликс', 'Ирина', 'Bliks_Irina']
        create_mail(line[2], line[0], line[1], 4)  # Отдел 4 = @ДРУЗЬЯ_ШКОЛЫ
        print(randompassword())


def create_femaly_mail():
    """ Русские только Фамилия (для почт тех кто в команде)"""
    for line in list_fio.splitlines():
        # Когда копирю из Google Sheets разделитель = Tab
        line = line.split(' ')
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        line.append(transliterate.translit(line[0], reversed=True).replace("'", ""))
        print(line)
        password = randompassword()
        create_mail(line[2], line[0], line[1], 1, password)  # Отдел 1 = Все сотрудники
        print(password)


def create_login_mail():
    """ English login (для технических почт)"""
    for line in list_fio.splitlines():
        # Когда копирю из Google Sheets разделитель = Tab
        # Zoom 05	zoom05
        line = line.split('\t')
        # <class 'list'>: ['Zoom 05', 'zoom05']
        # Первое слово пойдет в Имя остальное в Фамилия
        line.append(line[0].split(' ', maxsplit=1))
        print(line)
        # ['Zoom 05', 'zoom05', ['Zoom', '05']]
        password = randompassword()
        print(line[1], line[2][1], line[2][0])
        create_mail(line[1], line[2][1], line[2][0], 3, password)  # Отдел 3 = @СПЕЦПОЧТЫ
        print(password)


def create_ftp_login():
    """ English login (для технических почт)"""
    for line in list_fio.splitlines():
        line = line.split(' ')
        print(transliterate.translit(line[0], reversed=True).replace("'", "").lower())
        print(randompassword(strong=True, long=12))


def create_mail(nickname_, secname_, name_, department_id_=1, password_=mypassword):
    """
    Create Yandex mail.
    :param nickname_: Login
    :param secname_: Second Name
    :param name_: First Name
    :param department_id_: Номер отдела ID (4 - это Друзья Школы)
    :param password_: Пароль (у Друзей Школы почтовый пароль один на всех)
    """
    try:
        # https://yandex.ru/dev/connect/directory/api/concepts/users/add-user-docpage/
        result = api.user_add(nickname=nickname_, password=password_, department_id=department_id_, secname=secname_,
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


def show_groups():
    """ Посмотреть список групп"""
    department_list = api.department_list_full()
    print(department_list)
    # [{'id': 1, 'name': 'Все сотрудники'}, {'id': 3, 'name': '@СПЕЦПОЧТЫ'}, {'id': 4, 'name': '@ДРУЗЬЯ_ШКОЛЫ'}]


def invalid():
    print("ОШИБОЧНЫЙ ВЫБОР!")


def exit_fn():
    exit(0)


if __name__ == "__main__":
    # Русские Имя и Фамилия (для Друзей Школы)
    # create_fio_mail()
    # Русские только Фамилия (для почт тех кто в команде)
    # create_femaly_mail()
    # English login (для технических почт)
    # create_login_mail()
    # Посмотреть список групп
    # show_groups()
    # while True:
    menu = {"1": ("Создание учёток для Друзей Школы", create_fio_mail),
            "2": ("Создание учёток для членов комманды", create_femaly_mail),
            "3": ("Создание технических учёток", create_login_mail),
            "4": ("Логин для FTP", create_ftp_login),
            "5": ("Посмотреть список групп", show_groups),
            "6": ("Выход", exit_fn)
            }
    for key in sorted(menu.keys()):
        print(key + ":" + menu[key][0])

    ans = input("Выберите вариант!")
    menu.get(ans, [None, invalid])[1]()

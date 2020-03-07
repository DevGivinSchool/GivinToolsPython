import yandex_mail
import password_generator
import yandex_connect
# На вход подаються строки: Фамилия;Имя (пока из list.py)
from list import list_fio
from utils import get_login
from utils import split_str


# TODO: На вход везде должно подаваться одно и тоже Фамилия + Имя + Login, если чего-то нет, то оно собирается из друго.

def create_team_mail():
    """ Русские только Фамилия (для почт тех кто в команде)"""
    for line in list_fio.splitlines():
        line = split_str(line)
        # ['Карякина', 'Наталья']
        login_ = get_login(line[0], None)
        password = password_generator.random_password(strong=True, long=8)
        # Отдел 1 = Все сотрудники
        result = None
        try:
            result = yandex_mail.create_yandex_mail(line[0], line[1], login_, password, department_id_=1)
        except yandex_connect.YandexConnectExceptionY as e:
            # print(e.args[0])
            if e.args[0] == 500 or e.args[0] == 409:
                print(f"Unhandled exception: Такой пользователь уже существует: "
                      f"{login_ + '@givinschool.org'}. Пробую еще раз Фамилия+Имя")
                try:
                    login_ = get_login(line[0], line[1])
                    result = yandex_mail.create_yandex_mail(line[0], line[1], login_, password, department_id_=1)
                except yandex_connect.YandexConnectExceptionY as e:
                    if e.args[0] == 500 or e.args[0] == 409:
                        print(f"Unhandled exception: Такой пользователь уже существует: "
                              f"{login_ + '@givinschool.org'}.")
                    else:
                        print("ERROR = " + e.__str__())
            else:
                print("ERROR = " + e.__str__())
        # print(password)
        if result is not None:
            print(create_info_str(result))


def create_login_mail():
    """ English login (для технических почт)"""
    for line in list_fio.splitlines():
        # На вход подаються Фамилия Имя Логин
        # Отдел Кадров	hr
        line = split_str(line)
        print(line)
        login = line[1].lower()
        familia = line[0]
        name = line[1]
        password = password_generator.random_password(strong=True, long=8)
        print(familia, name, login)
        # Отдел 3 = @СПЕЦПОЧТЫ
        try:
            result = yandex_mail.create_yandex_mail(familia, name, login, password, department_id_=3)
        except yandex_connect.YandexConnectExceptionY as e:
            # print(e.args[0])
            if e.args[0] == 500:
                print(f"Unhandled exception: Такой пользователь уже существует: "
                      f"{login + '@givinschool.org'}")
            else:
                print("ERROR = " + e.__str__())
        print(create_info_str(result))


def create_ftp_login():
    """ FTP login (для ftp сервера)"""
    for line in list_fio.splitlines():
        line = split_str(line)
        # ['Карякина', 'Наталья']
        login_ = get_login(line[0], None)
        # print(f"Login: {translit_name(line[0]).lower()}")
        # print(f"Password: {password_generator.random_password(strong=True, long=12)}")
        # print("-"*45)
        # Так удобнее сразу копировать в таблицу
        print(login_ + "\t" + password_generator.random_password(strong=True, long=12))
        print("=" * 45)


def show_groups():
    """ Посмотреть список групп"""
    department_list = yandex_mail.show_groups()
    print(department_list)
    # [{'id': 1, 'name': 'Все сотрудники'}, {'id': 3, 'name': '@СПЕЦПОЧТЫ'}, {'id': 4, 'name': '@ДРУЗЬЯ_ШКОЛЫ'}]


def generate_password():
    s = 7
    while s not in [0, 1]:
        s = int(input("Строгий пароль (цифры и спецсимволы)? 0-Нет; 1-Да:"))
    z = 7
    while z not in [0, 1]:
        z = int(input("Пароль для Zoom? 0-Нет; 1-Да:"))
    ln = int(input("Длина пароля (по умолчанию 10 символов):") or 10)
    print(f"Пароль: {password_generator.random_password(strong=s, zoom=z, long=ln)}")


def create_info_str(result, password=True, welcome=True):
    text = ""
    text = text + f"Для: {result['name']['last']} {result['name']['first']}\n"
    text = text + f"Создана почта: {result['email']}\n"
    if password:
        text = text + f"Пароль: {result['password_']}\n"
    if welcome:
        text = text + f"Привет {result['name']['last']} {result['name']['first']}. " \
                      f"Твоя почта в Школе Гивина (Яндека.Почта - https://mail.yandex.ru)." \
                      f" Для входа используй имя - {result['email']} и пароль - {result['password_']}\n"
    return text


def invalid():
    print("ОШИБОЧНЫЙ ВЫБОР!")


def exit_fn():
    exit(0)


if __name__ == "__main__":
    # Русские Имя и Фамилия (для Друзей Школы)
    # from_list_create_sf_mails()
    # Русские только Фамилия (для почт тех кто в команде)
    # create_team_mail()
    # English login (для технических почт)
    # create_login_mail()
    # Посмотреть список групп
    # show_groups()
    # while True:
    menu = {"1": ("Создание учёток для членов комманды", create_team_mail),
            "2": ("Создание технических учёток (для технических почт)", create_login_mail),
            "3": ("Логин для FTP", create_ftp_login),
            "4": ("Посмотреть список групп", show_groups),
            "5": ("Генерировать пароль", generate_password),
            "6": ("Выход", exit_fn)
            }
    for key in sorted(menu.keys()):
        print(key + ":" + menu[key][0])

    ans = input("Выберите вариант!")
    menu.get(ans, [None, invalid])[1]()

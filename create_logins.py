import yandex_mail
import password_generator
import yandex_connect
# На вход подаються строки: Фамилия;Имя (пока из list.py)
from list import list_fio
from utils import get_login


# TODO: На вход везде должно подаваться одно и тоже Фамилия + Имя + Login, если чего-то нет, то оно собирается из друго.

def split_str(line):
    line_ = line.split('\t', maxsplit=1)
    if len(line_) < 2:
        line_ = line.split(' ', maxsplit=1)
    else:
        raise Exception("ERROR: Строка ФИО не разделяется ни через пробел ни через табуляцию")
    print(f"line_={line_}; line_[0]={line_[0]}; line_[1]={line_[1]}")
    return line_


def from_list_create_sf_mails():
    """ Русские Имя и Фамилия (для Друзей Школы)"""
    for line in list_fio.splitlines():
        # Когда копирую из Google Sheets разделитель = Tab
        # Иванов	Иван
        line_ = split_str(line)
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        # ['Иванов', 'Иван']
        login_ = get_login(line_[0], line_[1])
        try:
            result = yandex_mail.create_yandex_mail(line_[0], line_[1], login_, department_id_=4)
            # Отдел 4 = @ДРУЗЬЯ_ШКОЛЫ
        except yandex_connect.YandexConnectExceptionY as e:
            # print(e.args[0])
            if e.args[0] == 500:
                print(f"Unhandled exception: Такой пользователь уже существует: "
                      f"{login_ + '@givinschool.org'}")
            else:
                print("ERROR = " + e.__str__())
        # Для почты стандартный пароль, а это пароль для Zoom
        print(create_info_str(result, password=False, welcome=False))
        print(f"Пароль для Zoom: {password_generator.random_password(strong=True, zoom=True)}")


def create_team_mail():
    """ Русские только Фамилия (для почт тех кто в команде)"""
    for line in list_fio.splitlines():
        line = split_str(line)
        # ['Карякина', 'Наталья']
        login_ = get_login(line[0], None)
        password = password_generator.random_password(strong=True, long=8)
        # Отдел 1 = Все сотрудники
        result = yandex_mail.create_yandex_mail(line[0], line[1], login_, password, department_id_=1)
        # print(password)
        print(create_info_str(result))


def create_login_mail():
    """ English login (для технических почт)"""
    for line in list_fio.splitlines():
        # Отдел Кадров	hr
        line = split_str(line)
        login = line[1].lower()
        familia = line[0]
        name = line[1]
        password = password_generator.random_password(strong=True, long=8)
        print(familia, name, login)
        # Отдел 3 = @СПЕЦПОЧТЫ
        result = yandex_mail.create_yandex_mail(familia, name, login, password, department_id_=3)
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
    menu = {"1": ("Создание учёток для Друзей Школы", from_list_create_sf_mails),
            "2": ("Создание учёток для членов комманды", create_team_mail),
            "3": ("Создание технических учёток (для технических почт)", create_login_mail),
            "4": ("Логин для FTP", create_ftp_login),
            "5": ("Посмотреть список групп", show_groups),
            "6": ("Генерировать пароль", generate_password),
            "7": ("Выход", exit_fn)
            }
    for key in sorted(menu.keys()):
        print(key + ":" + menu[key][0])

    ans = input("Выберите вариант!")
    menu.get(ans, [None, invalid])[1]()

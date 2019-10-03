import yandex_mail
import password_generator
import yandex_connect
# На вход подаються строки: Фамилия;Имя (пока из list.py)
from list import list_fio
from stuff import translit_name


def from_list_create_sf_mails():
    """ Русские Имя и Фамилия (для Друзей Школы)"""
    for line in list_fio.splitlines():
        # Когда копирую из Google Sheets разделитель = Tab
        # Иванов	Иван
        line = line.split('\t')
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        print(line)
        # ['Иванов', 'Иван']
        try:
            result = yandex_mail.create_yandex_mail(line[0], line[1], department_id_=4)
            # Отдел 4 = @ДРУЗЬЯ_ШКОЛЫ
        except yandex_connect.YandexConnectExceptionY as e:
            # print(e.args[0])
            if e.args[0] == 500:
                print(f"Unhandled exception: Такой пользователь уже существует: "
                      f"{translit_name(line[0]) + '_' + translit_name(line[1]) + '@givinschool.org'}")
            else:
                print("ERROR = " + e.__str__())
        # Для почты стандартный пароль, это пароль для Zoom
        print(create_info_str(result))
        print(f"Пароль для Zoom: {password_generator.random_password(strong=True, zoom=True)}")


def create_femaly_mail():
    """ Русские только Фамилия (для почт тех кто в команде)"""
    for line in list_fio.splitlines():
        line = line.split(' ')
        # print(line)
        password = password_generator.random_password(strong=True, long=8)
        # Отдел 1 = Все сотрудники
        result = yandex_mail.create_yandex_mail(line[0], line[1], translit_name(line[0]), password, department_id_=1)
        # print(password)
        print(create_info_str(result))


def create_login_mail():
    """ English login (для технических почт)"""
    for line in list_fio.splitlines():
        # Отдел Кадров	hr
        line = line.split('\t')  # Когда копирю из Google Sheets разделитель = Tab
        print(line)
        login = line[1].lower()
        line = line[0].split(' ', maxsplit=1)
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
        line = line.split(' ')
        # print(f"Login: {translit_name(line[0]).lower()}")
        # print(f"Password: {password_generator.random_password(strong=True, long=12)}")
        # print("-"*45)
        # Так удобнее сразу копировать в таблицу
        print(translit_name(line[0]).lower() + "\t" + password_generator.random_password(strong=True, long=12))


def show_groups():
    """ Посмотреть список групп"""
    department_list = yandex_mail.show_groups()
    print(department_list)
    # [{'id': 1, 'name': 'Все сотрудники'}, {'id': 3, 'name': '@СПЕЦПОЧТЫ'}, {'id': 4, 'name': '@ДРУЗЬЯ_ШКОЛЫ'}]


def create_info_str(result):
    print(f"Для: {result['name']['last']} {result['name']['first']}")
    print(f"Создана почта: {result['email']}")
    print(f"Пароль: {result['password_']}")
    return f"Привет {result['name']['last']} {result['name']['first']}. Твоя почта в Школе Гивина (Яндека.Почта - " \
           f"https://mail.yandex.ru). Для входа используй имя - {result['email']} и пароль - {result['password_']} "


def invalid():
    print("ОШИБОЧНЫЙ ВЫБОР!")


def exit_fn():
    exit(0)


if __name__ == "__main__":
    # Русские Имя и Фамилия (для Друзей Школы)
    # from_list_create_sf_mails()
    # Русские только Фамилия (для почт тех кто в команде)
    # create_femaly_mail()
    # English login (для технических почт)
    # create_login_mail()
    # Посмотреть список групп
    # show_groups()
    # while True:
    menu = {"1": ("Создание учёток для Друзей Школы", from_list_create_sf_mails),
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

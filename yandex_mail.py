import yandex_connect
import PASSWORDS
import logging
from stuff import translit_name


logger = logging.getLogger('DBPostgres')


def create_yandex_mail(familia_, name_, login_=None, password_=None, department_id_=1):
    """
    Create Yandex mail.
    :param login_: Login
    :param familia_: Second Name
    :param name_: First Name
    :param department_id_: Номер отдела ID (4 - это Друзья Школы)
    :param password_: Пароль (у Друзей Школы почтовый пароль один на всех)
    """
    api = get_api()
    # Если пароль пустой то пароль будет стандартный для ДЩ
    if password_ is None:
        password_ = PASSWORDS.logins['default_ymail_password']  # Единый пароль для всех создаваемых почт для ДШ
    print(password_)
    logger.debug(f"password_={password_}")
    # Если логин не задан, тогда делаем его вида familia_name
    if login_ is None:
        login_ = translit_name(familia_) + "_" + translit_name(name_)
    print(login_)
    logger.debug(f"login_={login_}")
    # https://yandex.ru/dev/connect/directory/api/concepts/users/add-user-docpage/
    result = api.user_add(nickname=login_, password=password_, department_id=department_id_, secname=familia_,
                          name=name_)
    print(result)
    logger.debug(f"result={result}")
    return result


def get_api():
    # Токен Яндекса, действует год
    token = PASSWORDS.logins['token_yandex']
    api = yandex_connect.YandexConnectDirectory(token, org_id=None)
    return api


def show_groups():
    """ Посмотреть список групп"""
    api = get_api()
    department_list = api.department_list_full()
    return department_list
    # [{'id': 1, 'name': 'Все сотрудники'}, {'id': 3, 'name': '@СПЕЦПОЧТЫ'}, {'id': 4, 'name': '@ДРУЗЬЯ_ШКОЛЫ'}]

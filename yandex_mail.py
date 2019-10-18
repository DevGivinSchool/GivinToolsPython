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
        # Единый пароль для всех создаваемых почт для ДШ
        password_ = PASSWORDS.logins['default_ymail_password']
    # print(password_)
    logger.debug(f"password_={password_}")
    # Если логин не задан, тогда делаем его вида familia_name
    if login_ is None:
        # У некоторых фамили и имена сложные = несколько слов через пробел, поэтому пробел заменяю на подчёркивание
        login_ = translit_name(familia_).replace(' ', '_') + "_" + translit_name(name_).replace(' ', '_')
    # print(login_)
    logger.debug(f"login_={login_}")
    # https://yandex.ru/dev/connect/directory/api/concepts/users/add-user-docpage/
    result = api.user_add(nickname=login_, password=password_, department_id=department_id_, secname=familia_,
                          name=name_)
    """
    result = {
    'about': None, 
    'name': {
        'last': 'Ремнев', 
        'first': 'Сергей'}, 
    'language': 'ru', 
    'contacts': [
        {'synthetic': True, 
        'alias': False, 
        'main': False, 
        'type': 'staff', 
        'value': 'https://staff.yandex.ru/remnev_sergej'}, 
        {'synthetic': True, 
        'alias': False, 
        'main': True, 
        'type': 'email', 
        'value': 'remnev_sergej@givinschool.org'}
        ], 
    'gender': 'male', 
    'id': 1130000040012028, 
    'user_type': 'user', 
    'email': 'remnev_sergej@givinschool.org', 
    'service_slug': None, 
    'nickname': 'remnev_sergej', 
    'birthday': None, 
    'role': 'user', 
    'groups': [], 
    'position': None, 
    'department': {
        'members_count': 262, 
        'description': 'Здесь находятся все созданные аккаунты для Друзей Школы. Пароли от почт: XXX', 
        'name': '@ДРУЗЬЯ_ШКОЛЫ', 
        'created': '2019-05-27T08:28:30.839880Z', 
        'heads_group_id': 13, 
        'org_id': 2520809, 
        'label': 'fr_sc', 
        'parent_id': 1, 
        'maillist_type': 'inbox', 
        'path': '1.4', 
        'removed': False, 
        'external_id': None, 
        'id': 4, 
        'aliases': []}, 
    'timezone': 'Europe/Moscow', 
    'is_dismissed': False, 
    'external_id': None, 
    'is_robot': False, 
    'aliases': []
    }"""
    # Добавить в возвращаемый словарь логин и пароль
    result.update({'login_': login_})
    result.update({'password_': password_})
    # print(result)
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

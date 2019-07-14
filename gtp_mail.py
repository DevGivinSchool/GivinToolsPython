from list import *
# На вход подаються строки
# Глотова,Елена,Glotova,Elena,Glotova_Еlena@givinschool.org

# from yandex_connect import YandexConnectDirectory
#import list
import yandex_connect

token = "AgAAAAAigT1GAAWzDIvhjOnmRE81mGDc2Xk5M2U"
mypassword = "HWrqCQR6Wd"

api = yandex_connect.YandexConnectDirectory(token, org_id=None)

department_list = api.department_list_full()

for line in str.splitlines():
    str1 = line.split(',')
    print(line)
    try:
        print(api.user_add(nickname=str1[0] + '_' + str1[1], password=mypassword, department_id=4, secname=str1[0],
                           name=str1[1]))
    except yandex_connect.YandexConnectExceptionY as e:
        print("ERROR = " + e.__str__())

# {'about': None, 'name': {'last': '', 'first': ''}, 'language': 'ru', 'contacts': [{'synthetic': True, 'alias': False, 'main': False, 'type': 'staff', 'value': 'https://staff.yandex.ru/test1234'}, {'synthetic': True, 'alias': False, 'main': True, 'type': 'email', 'value': 'test1234@givinschool.org'}], 'gender': 'male', 'id': 1130000038583918, 'user_type': 'user', 'email': 'test1234@givinschool.org', 'service_slug': None, 'nickname': 'test1234', 'birthday': None, 'role': 'user', 'groups': [], 'position': None, 'department': {'members_count': 0, 'description': 'Здесь находятся все созданные аккаунты для Друзей Школы. Пароли от почт: HWrqCQR6Wd', 'name': '@ДРУЗЬЯ_ШКОЛЫ', 'created': '2019-05-27T08:28:30.839880Z', 'heads_group_id': 13, 'org_id': 2520809, 'label': 'fr_sc', 'parent_id': 1, 'maillist_type': 'inbox', 'path': '1.4', 'removed': False, 'external_id': None, 'id': 4, 'aliases': []}, 'timezone': 'Europe/Moscow', 'is_dismissed': False, 'external_id': None, 'is_robot': False, 'aliases': []}


"""
list_users = api.user_list_full()
print(api.user_list_full())  # просмотр всех сотрудников
print(api.department_list_full())
print(api.group_list_full())

# list_users = sorted(list_users, key = lambda i: i['nickname'])
#
# list_users1 = []
# for name in list_users:
#     list_users1.append(name['nickname'])
#     print(name['nickname'])
"""

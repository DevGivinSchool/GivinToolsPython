import random
import re
import string
password = 'vbsJuNDaMh'
print(password)
if not re.search(r'\d', password):
    password = password[:2] + random.choice(string.digits) + password[2 + 1:]
    #s = s[:num] + new_simbol + s[num + 1:]
    print(password)


"""
import string
import random


def randompassword():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # size = random.randint(8, 12) # Размер пароля всегда 10 символов
    size = 10
    password = ''.join(random.choice(chars) for x in range(size))
    # Заменить все буквы которые могут быть неправильно поняты пользователями
    for ch in ['l', 'j', 'i', '0', 'o', 'O']:
        if ch in password:
            password = password.replace(ch, random.choice(chars))
    return password


for i in range(15):
    print(randompassword())
"""

# import requests
#
# r = requests.get('https://newhuman.bitrix24.ru/oauth/authorize/?client_id=local.5d2a0084b949b0.22675909&response_type=code')
#
# print(r.content.decode())
# import json

# str = """(500, {'message': 'Unhandled exception: {error}', 'code': 'unhandled_exception', 'params': {'error': 'error'}}, 'https://api.directory.yandex.net/v6/users/', {'headers': {'Authorization': 'OAuth AgAAAAAigT1GAAWzDIvhjOnmRE81mGDc2Xk5M2U', 'Content-Type': 'application/json'}, 'data': '{"nickname": "Vernigorodskij_Andrej", "password": "HWrqCQR6Wd", "department_id": 4, "gender": "male", "name": {"first": "\\u0410\\u043d\\u0434\\u0440\\u0435\\u0439", "last": "\\u0412\\u0435\\u0440\\u043d\\u0438\\u0433\\u043e\\u0440\\u043e\\u0434\\u0441\\u043a\\u0438\\u0439"}}'})"""
# str2 = "{'message': 'Unhandled exception: {error}', 'code': 'unhandled_exception', 'params': {'error': 'error'}}"
# print(list(str))
# print(list(str2))
# print(json.dumps(str2, sort_keys=True, indent=4))
# print(json.loads(str))

# str3 = "{'about': None, 'name': {'last': 'Броди', 'first': 'Дмитрий'}, 'language': 'ru', 'contacts': [{'synthetic': True, 'alias': False, 'main': False, 'type': 'staff', 'value': 'https://staff.yandex.ru/brodi_dmitrij'}, {'synthetic': True, 'alias': False, 'main': True, 'type': 'email', 'value': 'brodi_dmitrij@givinschool.org'}], 'gender': 'male', 'id': 1130000039506321, 'user_type': 'user', 'email': 'brodi_dmitrij@givinschool.org', 'service_slug': None, 'nickname': 'brodi_dmitrij', 'birthday': None, 'role': 'user', 'groups': [], 'position': None, 'department': {'members_count': 224, 'description': 'Здесь находятся все созданные аккаунты для Друзей Школы. Пароли от почт: HWrqCQR6Wd', 'name': '@ДРУЗЬЯ_ШКОЛЫ', 'created': '2019-05-27T08:28:30.839880Z', 'heads_group_id': 13, 'org_id': 2520809, 'label': 'fr_sc', 'parent_id': 1, 'maillist_type': 'inbox', 'path': '1.4', 'removed': False, 'external_id': None, 'id': 4, 'aliases': []}, 'timezone': 'Europe/Moscow', 'is_dismissed': False, 'external_id': None, 'is_robot': False, 'aliases': []}"
# obj1 = (json.dumps(str3))
# obj1 = (json.loads(str3))
# obj1 = dict(str3)
# print(type(obj1))
# print(obj1)

# import os
#
# print(os.path.realpath(__file__))
# print(os.path.dirname(os.path.realpath(__file__)))



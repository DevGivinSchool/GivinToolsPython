# На вход подаються строки: Фамилия;Имя (пока из list.py)
from list import list_fio

import transliterate
import yandex_connect

# Токен Яндекса, действует год
token = "AgAAAAAigT1GAAWzDIvhjOnmRE81mGDc2Xk5M2U"
# Единый пароль для всех создаваемых почт
mypassword = "HWrqCQR6Wd"

api = yandex_connect.YandexConnectDirectory(token, org_id=None)

# Посмотреть список групп
# department_list = api.department_list_full()
# print(department_list)
# {'id': 4, 'name': '@ДРУЗЬЯ_ШКОЛЫ'}

for line in list_fio.splitlines():
    line = line.split(' ')
    line.append(transliterate.translit(line[0], reversed=True) + "_" + transliterate.translit(line[1], reversed=True))
    print(line)
    try:
        # https://yandex.ru/dev/connect/directory/api/concepts/users/add-user-docpage/
        print(api.user_add(nickname=line[2], password=mypassword, department_id=4, secname=line[0],
                           name=line[1]))
    except yandex_connect.YandexConnectExceptionY as e:
        #print(e.args[0])
        if e.args[0] == 500:
            print("Unhandled exception: Такой пользователь уже существует")
        else:
            print("ERROR = " + e.__str__())

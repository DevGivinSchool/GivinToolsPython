import requests
import json
import core.PASSWORDS as PASSWORDS


def getcourse_create_user():
    url = "https://givinschoolru.getcourse.ru/pl/api/users"
    headers = {"Content-Type": "application/json"}
    user = {
        "action": "add",
        "key": PASSWORDS.settings['getcourse_key'],
        "params": {
            "user": {
                "email": "email",
                "phone": "телефон",
                "first_name": "имя",
                "last_name": "фамилия",
                "city": "город",
                "country": "страна",

                "addfields": {"Доп.поле1": "значение", "Доп.поле2": "значение"}
            },
            "system": {
                "refresh_if_exists": 0,  # обновлять
                "partner_email": "email партнера (для пользователя)*",
            },
            "session": {
                "utm_source": "",
                "utm_medium": "",
                "utm_content": "",
                "utm_campaign": "",
                "utm_group": "",
                "gcpc": "",
                "gcao": "",
                "referer": "",
            }
        }
    }

    user = json.dumps(user)

    response = requests.request("POST", url, data=user, headers=headers)

    print(response)
    print(response.text)


def getcourse_get_fields():
    url = "https://givinschoolru.getcourse.ru/pl/api/account/fields"
    headers = {"Content-Type": "application/json"}
    data_array = {
        "action": "get",
        "key": PASSWORDS.settings['getcourse_key']
    }
    print(data_array)
    data_array = json.dumps(data_array)
    print(data_array)
    response = requests.request("POST", url, data=data_array, headers=headers)
    print(response)
    print(response.text)


if __name__ == '__main__':
    # getcourse_create_user()
    getcourse_get_fields()

#!/usr/bin/env python3
import requests
import json
import PASSWORDS


def http_get(url):
    answer = requests.get(url)
    result = answer.json()
    return result


def get_me():
    url = PASSWORDS.logins['telegram_bot_url'] + "/getMe"
    print(url)
    me = http_get(url)
    return me


def get_chat():
    url = PASSWORDS.logins['telegram_bot_url'] + "/getChat"
    print(url)
    channel_id = "@BobrD"

    r = requests.post(url, data={
        # "chat_id": 324846110
        "chat_id": "@BobrD"
    })
    # b'{"ok":false,"error_code":401,"description":"Unauthorized"}'
    print(r)
    parsed = json.loads(r.content)
    print(parsed)
    if not r.ok:
        # parsed = json.loads(r.content)
        if parsed['error_code'] == 401:
            raise Exception("401.Unauthorized")


def send_telegram(text: str):
    url = PASSWORDS.logins['telegram_bot_url'] + "/sendMessage"
    print(url)
    channel_id = "@BobrD"

    r = requests.post(url, data={
        "chat_id": "@BobrD".lower(),
        # "chat_id": 324846110,
        "text": text
    })
    # b'{"ok":false,"error_code":401,"description":"Unauthorized"}'
    print(r)
    parsed = json.loads(r.content)
    print(parsed)
    if not r.ok:
        # parsed = json.loads(r.content)
        if parsed['error_code'] == 401:
            raise Exception("401.Unauthorized")


if __name__ == '__main__':
    # send_telegram("hello world!")
    # print(get_me())
    # print(get_chat())

    import requests

    telegram_bot_url = 'https://api.telegram.org/bot1210796522:AAHfPgXkYrqPSakpsxB81UTsYwfmaq9dryY/'
    params_name = {'chat_id': '@BobrD', 'text': 'test777'}
    params_id = {'chat_id': 324846110, 'text': 'test777'}
    print("ID")
    response = requests.post(telegram_bot_url + 'sendMessage', data=params_id)
    print(response.json())
    print("USERNAME")
    response = requests.post(telegram_bot_url + 'sendMessage', data=params_name)
    print(response.json())
    # METHOD GET
    # response = requests.get(telegram_bot_url + 'sendMessage', params=params)
    # print(response.json())

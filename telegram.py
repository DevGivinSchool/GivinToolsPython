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
    print(get_chat())

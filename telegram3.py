import requests
import PASSWORDS

# telegram_bot_url = 'https://api.telegram.org/bot1210796522:AAHfPgXkYrqPSakpsxB81UTsYwfmaq9dryY/'


def get_chat_id(dictionary):
    """
    Method to extract chat id from telegram request.
    """
    chat_id = dictionary['message']['chat']['id']
    return chat_id


def get_message(dictionary):
    """
    Method to extract message id from telegram request.
    """
    message_text = dictionary['message']['text']
    return message_text


def get_updates_json(bot_url):
    params = {'timeout': 100, 'offset': None}
    response = requests.get(bot_url + '/getUpdates', data=params)
    print(response)
    print(response.json())
    return response.json()


# def last_update(data):
#     results = data['result']
#     print(results)
#     total_updates = len(results) - 1
#     print(total_updates)
#     print(results[total_updates])
#     return results[total_updates]


def get_chat_id(dictionary):
    chat_id = dictionary['message']['chat']['id']
    print(chat_id)
    return chat_id


def send_text_message(bot_url, chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(bot_url + '/sendMessage', data=params)
    print(response)
    return response


if __name__ == '__main__':
    updates = get_updates_json(PASSWORDS.logins['telegram_bot_url'])
    # lu = last_update(updates)
    for lu in updates['result']:
        chat_id = get_chat_id(lu)
    send_text_message(PASSWORDS.logins['telegram_bot_url'], chat_id, 'Your message goes here')


"""
<Response [200]>
{'ok': True, 'result': [{'update_id': 391387715, 'message': {'message_id': 20, 'from': {'id': 324846110, 'is_bot': False, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'language_code': 'ru'}, 'chat': {'id': 324846110, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'type': 'private'}, 'date': 1593108194, 'text': 'Test for link www.mail.ru  dsfhdsjfadsjf 3254', 'entities': [{'offset': 14, 'length': 11, 'type': 'url'}]}}]}
[{'update_id': 391387715, 'message': {'message_id': 20, 'from': {'id': 324846110, 'is_bot': False, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'language_code': 'ru'}, 'chat': {'id': 324846110, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'type': 'private'}, 'date': 1593108194, 'text': 'Test for link www.mail.ru  dsfhdsjfadsjf 3254', 'entities': [{'offset': 14, 'length': 11, 'type': 'url'}]}}]
0
{'update_id': 391387715, 'message': {'message_id': 20, 'from': {'id': 324846110, 'is_bot': False, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'language_code': 'ru'}, 'chat': {'id': 324846110, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'type': 'private'}, 'date': 1593108194, 'text': 'Test for link www.mail.ru  dsfhdsjfadsjf 3254', 'entities': [{'offset': 14, 'length': 11, 'type': 'url'}]}}
324846110
<Response [200]>
"""
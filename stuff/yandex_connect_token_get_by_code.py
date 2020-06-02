# from yandex_connect import token_get_by_code
# token = token_get_by_code()

# Выдернул процедуру получения токена Яндекс, т.к. неудобно вручную каждый раз вводить ID и т.п.
import base64
import PASSWORDS


def token_get_by_code():
    import requests
    client_id = PASSWORDS.logins['gtp_mail_robot_ID']
    client_secret = PASSWORDS.logins['gtp_mail_robot_password']
    print('Open link in browser:')
    print('https://oauth.yandex.ru/authorize?response_type=code&client_id=%s' % client_id)
    code = input('Enter code: ')

    auth = '%s:%s' % (client_id, client_secret)
    auth_base64 = base64.encodestring(auth.encode()).decode("utf-8")
    headers = {
        "Authorization": "Basic %s" % auth_base64.replace('\n', '').strip()
    }
    r = requests.post(
        'https://oauth.yandex.ru/token',
        headers=headers,
        data={
            'grant_type': 'authorization_code',
            'code': code
        }
    )
    print(r.text)


if __name__ == '__main__':
    token_get_by_code()

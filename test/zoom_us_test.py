from zoomus import ZoomClient
import json
import PASSWORDS
# import pprint
import requests
import time
import jwt


def generate_jwt(key, secret):
    header = {"alg": "HS256", "typ": "JWT"}

    payload = {"iss": key, "exp": int(time.time() + 3600)}

    token = jwt.encode(payload, secret, algorithm="HS256", headers=header)
    return token.decode("utf-8")


url = "https://api.zoom.us/v2/users"
# pp = pprint.PrettyPrinter(indent=4)
client = ZoomClient(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret'])

user = {
    "action": "string",
    "user_info": {
        "email": "string",
        "type": "integer",
        "first_name": "string",
        "last_name": "string",
        "password": "string"
    }
}

user['action'] = "autoCreate"
user['user_info']['email'] = "test777_test777@givinschool.org"
user['user_info']['type'] = 1
user['user_info']['first_name'] = "Дмитрий"
user['user_info']['last_name'] = "Салтыков Щедрин"
user['user_info']['password'] = "ANps11CDkz"
print(f"user={user}")
user_json = json.dumps(user)
print(f"user josn={user_json}")

myjwt = generate_jwt(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret'])
bearer = f"Bearer {myjwt}"
payload = user_json
headers = {
    'authorization': bearer,
    'content-type': "application/json"
}

# response = requests.request("POST", url, data=payload, headers=headers)
response = client.user.create(**user)

print(response.text)
print(f"respons={response}")
print(f"respons.headers={response.headers}")
print(f"respons.request.headers={response.request.headers}")
print(f"respons.request.path_url={response.request.path_url}")
print(f"respons.text={response.text}")
print(f"respons.url={response.url}")
print(f"response.status_code={response.status_code}") # 201 = ОК если нет тогда из str:response.text можно вытащить дополнительный код и сообщение

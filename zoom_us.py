from zoomus import ZoomClient
import json
import PASSWORDS
# import pprint

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
user['user_info']['type'] = "1"
user['user_info']['first_name'] = "Дмитрий"
user['user_info']['last_name'] = "Салтыков Щедрин"
user['user_info']['password'] = "ANps11CDkz"
print(f"user={user}")
user_json = json.dumps(user)
print(f"user josn={user_json}")

respons = client.user.create(**user)
print(f"respons={respons}")
print(f"respons.headers={respons.headers}")
print(f"respons.request.headers={respons.request.headers}")
print(f"respons.request.path_url={respons.request.path_url}")
print(f"respons.text={respons.text}")
print(f"respons.url={respons.url}")

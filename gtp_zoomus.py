from zoomus import ZoomClient
import json
import PASSWORDS

# client = ZoomClient('API_KEY', 'API_SECRET')
# client = ZoomClient(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret'])

"""
print(client.user.list().content)
print(json.loads(client.user.list().content))
print(json.loads(client.user.list().content)['users'])
print("="*60)
for user in json.loads(client.user.list().content)['users']:
    print(user)
    user_id = user['id']
    print(client.meeting.list(host_id=user_id))
"""
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

print(user['action'])

user['action'] = "autoCreate"
user['user_info']['email'] = "test777_test777@givinschool.org"
user['user_info']['type'] = "1"
user['user_info']['first_name'] = "Дмитрий"
user['user_info']['last_name'] = "Салтыков Щедрин"
user['user_info']['password'] = "ANps11CDkz"

print(user)

user_json = json.dumps(user)

print(user_json)

client = ZoomClient(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret'])

print(client.user.create(**user))

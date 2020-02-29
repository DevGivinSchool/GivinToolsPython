from zoomus import ZoomClient
import json
import PASSWORDS
import pprint
import re

client = ZoomClient(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret'])

# Список пользователей
# print(client.user.list().content)
# Список пользователей (словарь)
# print(json.loads(client.user.list().content))
# Список пользователей (словарь) чистый без дополнительной информации
# print(json.loads(client.user.list().content)['users'])
# print("=" * 80)
for user in sorted(json.loads(client.user.list().content)['users'], key=lambda i: i['email']):
    # pprint.pprint(user)
    # if user['email'].startswith('zoom'):
    if re.match(r"zoom\d{2}@givinschool.org", user['email']) is not None:
        # pp.pprint(user)
        print(f"email={user['email']}")
        # print(json.loads(client.meeting.list(user_id=user['id']).content))
        for meet in json.loads(client.meeting.list(user_id=user['id']).content)['meetings']:
            # print(meet)
            # print(f"    topic={meet['topic']}\n    url={meet['join_url']}")
            print(f'    "{meet["topic"]}" - {meet["join_url"]}')
    else:
        continue

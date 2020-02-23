from zoomus import ZoomClient
import json
import PASSWORDS
import pprint


client = ZoomClient(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret'])

# Список пользователей
# print(client.user.list().content)
# Список пользователей (словарь)
# print(json.loads(client.user.list().content))
# Список пользователей (словарь) чистый без дополнительной информации
# print(json.loads(client.user.list().content)['users'])
# print("=" * 80)
for user in json.loads(client.user.list().content)['users']:
    # pprint.pprint(user)
    if user['email'].startswith('zoom'):
        # pp.pprint(user)
        print(f"email={user['email']}")
        # print(json.loads(client.meeting.list(user_id=user['id']).content))
        for meet in json.loads(client.meeting.list(user_id=user['id']).content)['meetings']:
            # print(meet)
            # print(f"    topic={meet['topic']}\n    url={meet['join_url']}")
            print(f'    "{meet["topic"]}" - {meet["join_url"]}')
    else:
        continue

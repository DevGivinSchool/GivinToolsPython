import json
import PASSWORDS
import re
from zoomus import ZoomClient
from datetime import date

"""Zoom API
https://marketplace.zoom.us/docs/api-reference/introduction
"""

client = ZoomClient(PASSWORDS.logins['zoom_api_key'], PASSWORDS.logins['zoom_api_secret'])
print(f"Текущие встречи на {date.today()}:\n")
for user in sorted(json.loads(client.user.list().content)['users'], key=lambda i: i['email']):
    if re.match(r"zoom\d{2}@givinschool.org", user['email']) is not None:
        print(user['email'])
        for meet in json.loads(client.meeting.list(user_id=user['id']).content)['meetings']:
            # {'uuid': 'VMLPL4s2S5Se1e+rLwrd7w==', 'id': 618717733, 'host_id': 'IS5Fgs4XTEa-dknKFzNQWw', 'topic': 'ПТО  24.09-.05.10.2019', 'type': 8, 'start_time': '2019-09-28T05:00:00Z', 'duration': 240, 'timezone': 'Europe/Moscow', 'created_at': '2019-09-28T04:51:36Z', 'join_url': 'https://givinschool.zoom.us/j/618717733'}
            if meet["type"] == 3:
                # TODO Нужно добавить проверку type 8 и start_time >= now

                #  type 3 встречи без даты
                #  type 8 встречи на определенную дату (в список попадают и уже прошедшие встречи)
                id_ = str(meet["id"])
                id_ = id_[0:3] + "-" + id_[3:6] + "-" + id_[6:]
                print(f'    {meet["topic"]} - {id_} - {meet["join_url"]}')
    else:
        continue

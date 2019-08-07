from zoomus import ZoomClient
import json

#client = ZoomClient('API_KEY', 'API_SECRET')
client = ZoomClient('7dtr8NY6Q2m91uN0TQnfeQ', 'TyAcDcUBO2ZIns9g8cbc5Kgf5IB2Q71vAsOv')

print(client.user.list().content)
print(json.loads(client.user.list().content))
print(json.loads(client.user.list().content)['users'])
print("="*60)
for user in json.loads(client.user.list().content)['users']:
    print(user)
    user_id = user['id']
    print(client.meeting.list(host_id=user_id))



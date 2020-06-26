import requests

telegram_bot_url = 'https://api.telegram.org/bot1210796522:AAHfPgXkYrqPSakpsxB81UTsYwfmaq9dryY/'
params_name = {'chat_id': '@BobrD', 'text': 'test777'}
params_id = {'chat_id': 324846110, 'text': 'test777'}
print("ID")
response = requests.post(telegram_bot_url + 'sendMessage', data=params_id)
print(response.json())
print("USERNAME")
response = requests.post(telegram_bot_url + 'sendMessage', data=params_name)
print(response.json())
# METHOD GET
# response = requests.get(telegram_bot_url + 'sendMessage', params=params)
# print(response.json())

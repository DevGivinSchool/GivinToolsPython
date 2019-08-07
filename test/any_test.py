import requests

r = requests.get('https://newhuman.bitrix24.ru/oauth/authorize/?client_id=local.5d2a0084b949b0.22675909&response_type=code')

print(r.content.decode())


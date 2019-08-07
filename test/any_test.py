# import requests
#
# r = requests.get('https://newhuman.bitrix24.ru/oauth/authorize/?client_id=local.5d2a0084b949b0.22675909&response_type=code')
#
# print(r.content.decode())
import json

str = """(500, {'message': 'Unhandled exception: {error}', 'code': 'unhandled_exception', 'params': {'error': 'error'}}, 'https://api.directory.yandex.net/v6/users/', {'headers': {'Authorization': 'OAuth AgAAAAAigT1GAAWzDIvhjOnmRE81mGDc2Xk5M2U', 'Content-Type': 'application/json'}, 'data': '{"nickname": "Vernigorodskij_Andrej", "password": "HWrqCQR6Wd", "department_id": 4, "gender": "male", "name": {"first": "\\u0410\\u043d\\u0434\\u0440\\u0435\\u0439", "last": "\\u0412\\u0435\\u0440\\u043d\\u0438\\u0433\\u043e\\u0440\\u043e\\u0434\\u0441\\u043a\\u0438\\u0439"}}'})"""
str2 = "{'message': 'Unhandled exception: {error}', 'code': 'unhandled_exception', 'params': {'error': 'error'}}"
#print(list(str))
#print(list(str2))
print(json.dumps(str2, sort_keys=True, indent=4))
#print(json.loads(str))
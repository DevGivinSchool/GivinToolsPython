"""
import datetime

print(datetime.date(2019, 10, 10) + datetime.timedelta(days=97))
"""


# процедура блокировки пользователя
import datetime
import string
import re
import PASSWORDS
import config
from DBPostgres import DBPostgres


list_participants = """@Akmaral1111
  САМАРИЧЕВ АнДРЕЙ 
@telegram1
wwww@mail.ru
иванов иван
van der bild
"""

# Подключение к БД
postgres = DBPostgres(dbname=config.config['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                      password=PASSWORDS.logins['postgres_password'], host=config.config['postgres_host'],
                      port=config.config['postgres_port'])
pattern_eng = re.compile("[A-Za-z]+")
pattern_rus = re.compile("[А-Яа-я]+")
for p in list_participants.splitlines():
    print(f"Попытка блокировки участника {p}")
    p = p.strip()
    participant_id = None
    if p[0] == '@':
        # Ищем участника по Telegram
        sql_instr = "telegram"
        p = p.lower()
        print(f"Ищем участника по Telegram - {p}")
        participant_id = postgres.find_participant_by('telegram', p)
    elif '@' in p:
        # Ищем участника по email
        sql_instr = "email"
        p = p.lower()
        print(f"Ищем участника по email - {p}")
        participant_id = postgres.find_participant_by('email', p)
    elif pattern_rus.match(p.replace(' ', '')):
        # Ищем участника по fio
        sql_instr = "fio"
        p = p.upper()
        print(f"Ищем участника по fio - {p}")
        participant_id = postgres.find_participant_by('fio', p)
    elif pattern_eng.match(p.replace(' ', '')):
        # Ищем участника по fio_eng
        sql_instr = "fio_eng"
        p = p.upper()
        print(f"Ищем участника по fio_eng - {p}")
        participant_id = postgres.find_participant_by('fio_eng', p)
    if participant_id is None:
        print(f"******* ВНИМАНИЕ: По значению {p} ничего не нашлось")
        print("-" * 45)
        continue
    # Блокируем пользователя
    sql_text = f"UPDATE participants SET type='B', password=password||'55' where {sql_instr}=%s RETURNING id;"
    values_tuple = (p,)
    id_ = postgres.execute_dml_id(sql_text, values_tuple)
    if id_ is None:
        print(f"******* ВНИМАНИЕ: UPDATE для {p} не отработал")
    else:
        print(f"Заблокирован участник ID={id_}")
        # Состояние участник
        sql_text = 'SELECT id, fio, login, password, type FROM participants where id=%s;'
        values_tuple = (id_,)
        rows = postgres.execute_select(sql_text, values_tuple)
        print(rows)
        # TODO Послать письмо админу чтобы сменил пароль Zoom
    print("-"*45)
postgres.disconnect()


"""
# процедура создания нового участника
import datetime
import PASSWORDS
import config
from DBPostgres import DBPostgres

payment = {'payment_id': 389, 'participant_id': None, 'number_of_days': 30, 'deadline': datetime.datetime(2019, 11, 4, 10, 37, 56, 738229), 'Фамилия': 'ОТБОЕВА', 'Имя': 'ЛАРИСА', 'Фамилия Имя': 'ОТБОЕВА ЛАРИСА', 'Электронная почта': '', 'Наименование услуги': '1. Друзья Школы - 1 месяц (1 990 руб.)', 'ID платежа': '0784', 'Оплаченная сумма': 2060, 'Кассовый чек 54-ФЗ': 'https://givinschoolru.getcourse.ru/sales/control/deal/update/id/20876010', 'Время проведения': datetime.datetime(2019, 10, 5, 10, 37, 56, 738229), 'Номер карты': '', 'Тип карты': '', 'Защита 3-D Secure': '', 'Номер транзакции': '', 'Код авторизации': '', 'Платежная система': 1}
text = "Отбоева	Лариса	Otboevalarisa2016@gmail.com		otboeva_larisa@givinschool.org	xmX&htd4vb"
text = text.split("\t")
print(text)
if text[2]:
    email = text[2].lower()
else:
    email = None
if text[3]:
    telegram = text[3].lower()
else:
    telegram = None
login = text[4]
password = text[5]
if payment["Электронная почта"] is None:
    payment["Электронная почта"] = email

print(f'email={email}; email2={payment["Электронная почта"]}; telegram={telegram}; login={login}; password={password}')

# Подключение к БД
postgres = DBPostgres(dbname=config.config['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                      password=PASSWORDS.logins['postgres_password'], host=config.config['postgres_host'],
                      port=config.config['postgres_port'])

# Создаём нового пользователя в БД (оплата сразу отмечается и type='N')
sql_text = "INSERT INTO participants(last_name, first_name, fio, email, type, payment_date, number_of_days, deadline,
              telegram, login, password) 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
values_tuple = (payment["Фамилия"], payment["Имя"],
                payment["Фамилия Имя"], payment["Электронная почта"], 'N',
                payment["Время проведения"], payment["number_of_days"],
                payment["deadline"]
                , telegram, login, password)
payment["participant_id"] = postgres.execute_dml_id(sql_text, values_tuple)
print(payment["participant_id"])

# Прикрепить участника к платежу
sql_text = "UPDATE payments SET participant_id=%s WHERE task_uuid=%s;"
values_tuple = (payment["participant_id"], payment["payment_id"])
postgres.execute_dml(sql_text, values_tuple)

# Состояние участник
sql_text = 'SELECT * FROM participants where id=%s;'
values_tuple = (payment["participant_id"],)
rows = postgres.execute_select(sql_text, values_tuple)
print(rows)

postgres.disconnect()
"""

"""
# Посмотреть как что возвращает select, в какой форме
import PASSWORDS
import config
from DBPostgres import DBPostgres

postgres = DBPostgres(dbname=config.config['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                      password=PASSWORDS.logins['postgres_password'], host=config.config['postgres_host'],
                      port=config.config['postgres_port'])
sql_text = 'SELECT * FROM participants where id=%s;'
values_tuple = ('1182',)
rows = postgres.execute_select(sql_text, values_tuple)
print(rows)
# [(1182, 'КОЗЛОВА', 'СВЕТЛАНА', 'КОЗЛОВА СВЕТЛАНА', '89098169809@mail.ru', '@89098169809', datetime.datetime(2019, 10, 3, 17, 2, 18, 282109, tzinfo=psycopg2.tz.FixedOffsetTimezone(offset=180, name=None)), None, 'kozlova_svetlana@givinschool.org', 'dC22kH615u', datetime.date(2019, 10, 5), 30, datetime.date(2019, 11, 4), None, None, 'P')]
postgres.disconnect()
"""

"""
# Получить текскт sql запроса для логирования
sql_text = "UPDATE participants 
        SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type='P' 
        WHERE id=%s;"
values_tuple = ('one', 'two', '3333', '4444')
print(sql_text % values_tuple)
"""

"""
# Перемещение письма в почте в другую папку
from imapclient import IMAPClient
import PASSWORDS


def move_email_to_trash(server, emailid):
    # output = []
    # result = server.uid('MOVE', emailid, "Trash")
    result = server.move(emailid, "Trash")
    print(result)
    #output.append(result)
    #if result[0] == 'OK':
    #    result = mov, data = server.uid('STORE', emailid, '+FLAGS', '(\Deleted Items)')
    #    server.expunge()


client = IMAPClient(host="imap.yandex.ru", use_uid=True)
client.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
client.select_folder('INBOX')
messages = client.search('ALL')
print(messages)
# [260, 263, 271, 276, 280, 285]
# We go through the cycle in all letters
#for uid, message_data in client.fetch(messages, 'RFC822').items():
#    pass
move_email_to_trash(client, 260)
#result = client.get_flags(263)
print(result)
"""

"""
tab = {'about': None,
       'name': {'last': 'МИРОНЮК', 'first': 'НАТАЛЬЯ'},
       'language': 'ru',
       'contacts': [{'synthetic': True, 'alias': False, 'main': False, 'type': 'staff', 'value': 'https://staff.yandex.ru/mironjuk_natalja'}, {'synthetic': True, 'alias': False, 'main': True, 'type': 'email', 'value': 'mironjuk_natalja@givinschool.org'}],
       'gender': 'male',
       'id': 1130000039994353,
       'user_type': 'user',
       'email': 'mironjuk_natalja@givinschool.org',
       'service_slug': None,
       'nickname': 'mironjuk_natalja',
       'birthday': None,
       'role': 'user',
       'groups': [],
       'position': None,
       'department': {'members_count': 261, 'description': 'Здесь находятся все созданные аккаунты для Друзей Школы. Пароли от почт: HWrqCQR6Wd', 'name': '@ДРУЗЬЯ_ШКОЛЫ', 'created': '2019-05-27T08:28:30.839880Z', 'heads_group_id': 13, 'org_id': 2520809, 'label': 'fr_sc', 'parent_id': 1, 'maillist_type': 'inbox', 'path': '1.4', 'removed': False, 'external_id': None, 'id': 4, 'aliases': []},
       'timezone': 'Europe/Moscow',
       'is_dismissed': False,
       'external_id': None,
       'is_robot': False,
       'aliases': []
       }
print(tab['email'])
"""

"""
import datetime

today = datetime.datetime.now()
print(today)
print(today + datetime.timedelta(days=30))
print(today + datetime.timedelta(days=90))
print(today + datetime.timedelta(days=180))
today2 = datetime.datetime.strptime('2019-09-11 21:05:45', '%Y-%m-%d %H:%M:%S')
print(today2)
print(type(today2))
print(today2 + datetime.timedelta(days=30))
print(today2 + datetime.timedelta(days=90))
print(today2 + datetime.timedelta(days=180))
"""

"""
import string
import random
password = "password"

password = password[:-2] + random.choice(string.ascii_lowercase)*2
print(password)
"""

"""
# Создание пользователя Zoom
import requests
import PASSWORDS

url = "https://api.zoom.us/v2/users"

payload = "{\"action\":\"autoCreate\",\"user_info\":{\"email\":\"test777_test777@givinschool.org\",\"type\":\"1\",\"first_name\":\"Дмитрий\",\"last_name\":\"Салтыков Щедрин\",\"password\":\"ANps11CDkz\"}}"
print(type(payload))
payload = payload.encode('utf-8')
headers = {
    'content-type': "application/json",
    'authorization': PASSWORDS.logins['zoom_authorization']
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
"""

# import re
# sum = "1 990.00 руб."
# res = sum.split(".")[0].replace(" ","")
# print(res)

"""from lxml import html

with open(r"paykeeper.html", encoding="utf-8") as file:
    data = file.read()
tree = html.fromstring(data)
# print(tree)
# Вот такая строка XPath у меня сработала
# res = tree.xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[5]/tbody/tr/td[2]/table")
tables = tree.xpath('//table[@width="430"]')
# print(f"res={tables}")
tr = tables[0].xpath('.//tr')
# print(f"tr={tr}")
#print(f"tr2={tr[0].text_content()}")
td = tr[0].xpath('.//td')
print(f"td={td}")
text = td[0].text_content()
print(f"text={text}")
text = td[1].text_content().strip()
print(f"text={text}")
print("="*45)
for table in tables:
     trs = table.xpath('.//tr')
     print(f"tr={trs}")
     for td in trs:
         tds = td.xpath('.//td')
         print(f"tds={tds}")
         text = cell.text_content()
         # for cell in tds:
         #     print(f"cell={cell}")
         #     text = cell.text_content()
         #     print(f"text={text}")

"""

"""from lxml import html
test = '''
    <html>
        <body>
            <div class="first_level">
                <h2 align='center'>one</h2>
                <h2 align='left'>two</h2>
            </div>
            <h2>another tag</h2>
        </body>
    </html>
'''
tree = html.fromstring(test)
res = tree.xpath('//h2') # все h2 теги
print(res)
res = tree.xpath('//h2[@align]') # h2 теги с атрибутом align
print(res)
res = tree.xpath('//h2[@align="center"]') # h2 теги с атрибутом align равным "center"
print(res)
res = div_node = tree.xpath('//div')[0] # div тег
print(res)
res = div_node.xpath('.//h2') # все h2 теги, которые являются дочерними div ноде
print(res)"""

"""import random
import re
import string
password = 'vbsJuNDaMh'
print(password)
if not re.search(r'\d', password):
    password = password[:2] + random.choice(string.digits) + password[2 + 1:]
    #s = s[:num] + new_simbol + s[num + 1:]
    print(password)
"""

"""
import string
import random


def random_password():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # size = random.randint(8, 12) # Размер пароля всегда 10 символов
    size = 10
    password = ''.join(random.choice(chars) for x in range(size))
    # Заменить все буквы которые могут быть неправильно поняты пользователями
    for ch in ['l', 'j', 'i', '0', 'o', 'O']:
        if ch in password:
            password = password.replace(ch, random.choice(chars))
    return password


for i in range(15):
    print(random_password())
"""

# import requests
#
# r = requests.get('https://newhuman.bitrix24.ru/oauth/authorize/?client_id=local.5d2a0084b949b0.22675909&response_type=code')
#
# print(r.content.decode())
# import json

# str = """(500, {'message': 'Unhandled exception: {error}', 'code': 'unhandled_exception', 'params': {'error': 'error'}}, 'https://api.directory.yandex.net/v6/users/', {'headers': {'Authorization': 'OAuth AgAAAAAigT1GAAWzDIvhjOnmRE81mGDc2Xk5M2U', 'Content-Type': 'application/json'}, 'data': '{"nickname": "Vernigorodskij_Andrej", "password": "HWrqCQR6Wd", "department_id": 4, "gender": "male", "name": {"first": "\\u0410\\u043d\\u0434\\u0440\\u0435\\u0439", "last": "\\u0412\\u0435\\u0440\\u043d\\u0438\\u0433\\u043e\\u0440\\u043e\\u0434\\u0441\\u043a\\u0438\\u0439"}}'})"""
# str2 = "{'message': 'Unhandled exception: {error}', 'code': 'unhandled_exception', 'params': {'error': 'error'}}"
# print(list(str))
# print(list(str2))
# print(json.dumps(str2, sort_keys=True, indent=4))
# print(json.loads(str))

# str3 = "{'about': None, 'name': {'last': 'Броди', 'first': 'Дмитрий'}, 'language': 'ru', 'contacts': [{'synthetic': True, 'alias': False, 'main': False, 'type': 'staff', 'value': 'https://staff.yandex.ru/brodi_dmitrij'}, {'synthetic': True, 'alias': False, 'main': True, 'type': 'email', 'value': 'brodi_dmitrij@givinschool.org'}], 'gender': 'male', 'id': 1130000039506321, 'user_type': 'user', 'email': 'brodi_dmitrij@givinschool.org', 'service_slug': None, 'nickname': 'brodi_dmitrij', 'birthday': None, 'role': 'user', 'groups': [], 'position': None, 'department': {'members_count': 224, 'description': 'Здесь находятся все созданные аккаунты для Друзей Школы. Пароли от почт: HWrqCQR6Wd', 'name': '@ДРУЗЬЯ_ШКОЛЫ', 'created': '2019-05-27T08:28:30.839880Z', 'heads_group_id': 13, 'org_id': 2520809, 'label': 'fr_sc', 'parent_id': 1, 'maillist_type': 'inbox', 'path': '1.4', 'removed': False, 'external_id': None, 'id': 4, 'aliases': []}, 'timezone': 'Europe/Moscow', 'is_dismissed': False, 'external_id': None, 'is_robot': False, 'aliases': []}"
# obj1 = (json.dumps(str3))
# obj1 = (json.loads(str3))
# obj1 = dict(str3)
# print(type(obj1))
# print(obj1)

# import os
#
# print(os.path.realpath(__file__))
# print(os.path.dirname(os.path.realpath(__file__)))

import Parser
import log_config
from datetime import datetime
from Log import Log
from log_config import log_dir, log_level

body_html = """
<div class="message-from-gc">
	<table>
	<tr>
				<td valign="top">
			<div  style="">
			<img width='50' class='user-profile-image user-default-profile-image ' src='http://getcourse.ru/public/img/default_profile_50.png'>			</div>
		</td>
				<td>
			     Поступила оплата по заказу 1517 на сумму 150€ через PayPal.
    <BR><BR>

        Страница заказа: <a href='http://givin.school/g/4093964694/e079641a?v=MA3QzM1cDOy8CZp9SZ0FGZwV3LsFWZk9CbvJHdu92YvMXZsF2cvw2bvh2Yz5ibpZXan9yL6MHc0RHa'>https://givin.school/sales/control/deal/update/id/28753470</a>
    <BR><BR>

    Клиент: Диана Потёмкина<BR>
                                                                                            <br />
    Состав заказа:<br /><br />
            1. Интенсив "Жажда Жизни" Бад-Майнберг 11-15.03.2020 (380€)<br />
        <br />
					</td>
	</tr>
	<tr>
		<td colspan="2">
									<a href="http://givin.school/g/4093964694/e079641a?v=MA3QzM1cDOyYkMlQWaGJTJlRXYkBXdGJTJsFWZkZkMlw2byRnbvNmRyUyclxWYzZkMlw2bvh2Yz5ibpZXanZkMlYkMlE0MlMHc0RHa9wmc1ZyMyAzMwEjNyYTPkl2PrNWasN2Lz52bpRXYjlmZpR3bu9ycu9Wa0F2YpZWa09mbvw2bvh2Yz5ibpZXan9yL6MHc0RHa" style="font-family: arial; border: 0px; background: #428bca; font-size: 14px; padding: 7px 20px; color: white; display: inline-block; text-decoration: none;">Перейти</a>
					</td>
	</tr>
</table>
<div style="clear: both"></div>	<br />
	<br />
	<div class="footer" style="border-top: 1px solid #ddd">
				<BR>
							<span
				style="font-size: 0.8em; color: #999">Вы получили это письмо, потому что регистрировались в проекте &laquo;givinschoolru&raquo;</span>
			<BR>
			<span
				style="font-size: 0.8em; color: #999">Если вы не хотите получать письма от нас, вы можете				<a style="color: #999; "
				   href='http://givin.school/notifications/unsubscribe/message/id/4093964694/h/c1342'> отписаться</a></span>
									<img src="http://givin.school/notifications/messagePublic/view/id/4093964694/hash/e079641a" style="width: 0; height: 0; border: 0;" width="0" height="0" border="0" />
			</div>
</div>

2020-02-10 17:47:00,066|   ERROR| TASK ERROR:
Traceback (most recent call last):
  File "/home/robot/MyGit/GivinToolsPython/Email2.py", line 173, in sort_mail
    payment = Parser.parse_getcourse_html(body['body_html'], self.logger)
  File "/home/robot/MyGit/GivinToolsPython/Parser.py", line 104, in parse_getcourse_html
    payment["Оплаченная сумма"] = re.findall(r'на сумму.*руб.', line)[0] \
IndexError: list index out of range

2020-02-10 17:47:00,066|   ERROR| UUID: 1712
2020-02-10 17:47:00,066|   ERROR| FROM: info@givin.school
2020-02-10 17:47:00,066|   ERROR| SUBJECT: Поступил платеж - 150€ (PayPal)
2020-02-10 17:47:00,066|   ERROR| BODY
:  		 Поступила оплата по заказу 1517 на
сумму 150€ через PayPal. 

Страница заказа:
https://givin.school/sales/control/deal/update/id/28753470
[http://givin.school/g/4093964694/e079641a?v=MA3QzM1cDOy8CZp9SZ0FGZwV3LsFWZk9CbvJHdu92YvMXZsF2cvw2bvh2Yz5ibpZXan9yL6MHc0RHa]


Клиент: Диана Потёмкина

Состав заказа:

1. Интенсив "Жажда Жизни" Бад-Майнберг
11-15.03.2020 (380€)

 		 Перейти
[http://givin.school/g/4093964694/e079641a?v=MA3QzM1cDOyYkMlQWaGJTJlRXYkBXdGJTJsFWZkZkMlw2byRnbvNmRyUyclxWYzZkMlw2bvh2Yz5ibpZXanZkMlYkMlE0MlMHc0RHa9wmc1ZyMyAzMwEjNyYTPkl2PrNWasN2Lz52bpRXYjlmZpR3bu9ycu9Wa0F2YpZWa09mbvw2bvh2Yz5ibpZXan9yL6MHc0RHa]


Вы получили это письмо, потому что
регистрировались в проекте «givinschoolru» 
Если вы не хотите получать письма от
нас, вы можете отписаться
[http://givin.school/notifications/unsubscribe/message/id/4093964694/h/c1342]
 
Вы можете ознакомиться с HTML версией письма
пройдя по ссылке
[https://givin.school/pl/notifications/control/messages/html-version?id=4093964694&hash=e079641a]

"""
now = datetime.now().strftime("%Y%m%d%H%M")
logger = Log.setup_logger('__main__', log_dir, f'gtp_school_friends_{now}.log',
                          log_level)
payment = Parser.parse_getcourse_html(body_html, logger)


"""from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())"""

"""import datetime
#from string import Template
#t = Template('$id|$type|$family|$name|$email|$telegram|')
row = (1126, 'P', 'АБРАМОВА', 'ЕЛЕНА', 'el34513543@gmail.com', '', datetime.date(2019, 8, 7), 45,
       datetime.date(2019, 9, 21), datetime.date(2019, 10, 15), 'None')
w = (4, 3, 20, 20, 40, 40, 10, 4, 10, 10, 40)
print(f"{str(row[0]).ljust(w[0])}|{row[1].ljust(w[1])}|{row[2].ljust(w[2])}|"
      f"{row[3].ljust(w[3])}|{row[4].ljust(w[4])}|{row[5].ljust(w[5])}|"
      f"{row[6].strftime('%d.%m.%Y').ljust(w[6])}|{str(row[7]).ljust(w[7])}|"
      f"{row[8].strftime('%d.%m.%Y').ljust(w[8])}|{row[9].strftime('%d.%m.%Y').ljust(w[9])}|"
      f"{row[10].ljust(w[10])}|")
# Template(t).substitute(id=name, error=hex(errno))
row2 = set()
row3 = []
for i in row:
    row2.add(i)
    row3.append(i)
print(row2)
print(row3)"""

"""from datetime import datetime
item = '2019-08-07'
item = datetime.strptime(item, '%Y-%m-%d')
print(item)"""

"""
link = "https://givin.school/sales/control/deal/update/id/24611232"
link_id = link.rsplit("/", 1)
link = "https://givinschoolru.getcourse.ru/sales/control/deal/update/id/" + link_id[1]
print(link)
"""

"""import re
text = 'SCH_Mihail_Ivanenko вафйуцке @ddddd raetbr rter @telegram_name bbb, https://t.me/chigirigi fedgfsg купефук '
# mask = r'https://t.me/\w*'
mask = r'[a-zA-Z0-9_]+'
result = re.search(mask, text)
# result2 = re.search(mask, text)
# result = '@' + result.group(0).rsplit("/", 1)[1]
print(result.group(0))
print("exit")"""

"""
text = "Поступила оплата по заказу 1052 на сумму 2 2 руб. через Яндекс.Касса."
#q2 = re.findall(r'\d+ \d+ руб.', text)
q2 = re.findall(r'на сумму.*руб.', text)
print(q2)
print(len(q2))
q3 = q2[0]
print(q3)
q1 = q3.replace('на сумму ', '').replace(' руб.', '').replace(' ', '')
print(q1)
"""

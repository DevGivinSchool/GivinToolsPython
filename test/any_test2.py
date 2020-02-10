import Parser
import gtp_config
from datetime import datetime
from Log import Log


body_html = """
<div class="message-from-gc">
	<table>
	<tr>
				<td valign="top">
			<div  style="">
			<img width='50' class='user-profile-image ' src='http://fs-th02.getcourse.ru/fileservice/file/thumbnail/h/AB.fb16f6cdaa994ebf0d144241c1f50a0e.jpg/s/50x50/a/76390/sc/131'>			</div>
		</td>
				<td>
			     Поступила оплата по заказу 1584 на сумму 1 990 руб. через CloudPayments.
    <BR><BR>

        Страница заказа: <a href='http://givin.school/g/4099824594/ea19aaff?v=NA0cjM1ATOy8CZp9SZ0FGZwV3LsFWZk9CbvJHdu92YvMXZsF2cvw2bvh2Yz5ibpZXan9yL6MHc0RHa'>https://givin.school/sales/control/deal/update/id/29052744</a>
    <BR><BR>

    Клиент: Аделия Утешева<BR>
                                                                                            <br />
    Состав заказа:<br /><br />
            1. Друзья Школы - 1 месяц (1 990 руб.)<br />
        <br />
					</td>
	</tr>
	<tr>
		<td colspan="2">
									<a href="http://givin.school/g/4099824594/ea19aaff?v=NA0cjM1ATOyYkMlQWaGJTJlRXYkBXdGJTJsFWZkZkMlw2byRnbvNmRyUyclxWYzZkMlw2bvh2Yz5ibpZXanZkMlYkMlE0MlMHc0RHa9wmc1ZSM0ETOxkjNyYTPkl2PrNWasN2Lz52bpRXYjlmZpR3bu9ycu9Wa0F2YpZWa09mbvw2bvh2Yz5ibpZXan9yL6MHc0RHa" style="font-family: arial; border: 0px; background: #428bca; font-size: 14px; padding: 7px 20px; color: white; display: inline-block; text-decoration: none;">Перейти</a>
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
				   href='http://givin.school/notifications/unsubscribe/message/id/4099824594/h/6308d'> отписаться</a></span>
									<img src="http://givin.school/notifications/messagePublic/view/id/4099824594/hash/ea19aaff" style="width: 0; height: 0; border: 0;" width="0" height="0" border="0" />
			</div>
</div>
"""
now = datetime.now().strftime("%Y%m%d%H%M")
logger = Log.setup_logger('__main__', gtp_config.config['log_dir'], f'gtp_school_friends_{now}.log',
                          gtp_config.config['log_level'])
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

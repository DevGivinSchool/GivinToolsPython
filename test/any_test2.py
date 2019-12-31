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

import re
text = 'SCH_Mihail_Ivanenko вафйуцке @ddddd raetbr rter @telegram_name bbb, https://t.me/chigirigi fedgfsg купефук '
# mask = r'https://t.me/\w*'
mask = r'[a-zA-Z0-9_]+'
result = re.search(mask, text)
# result2 = re.search(mask, text)
# result = '@' + result.group(0).rsplit("/", 1)[1]
print(result.group(0))
print("exit")

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

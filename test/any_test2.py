from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

"""
link = "https://givin.school/sales/control/deal/update/id/24611232"
link_id = link.rsplit("/", 1)
link = "https://givinschoolru.getcourse.ru/sales/control/deal/update/id/" + link_id[1]
print(link)
"""


"""import re
text = '@ddddd raetbr rter @telegram_name bbb, https://t.me/chigirigi fedgfsg купефук '
mask = r'https://t.me/\w*'
result = re.search(mask, text)
result2 = re.search(mask, text)
result = '@' + result.group(0).rsplit("/", 1)[1]
print(result)
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

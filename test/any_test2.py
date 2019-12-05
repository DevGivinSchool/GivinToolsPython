import re

text = "Поступила оплата по заказу 1052 на сумму 2 2 руб. через Яндекс.Касса."
#q2 = re.findall(r'\d+ \d+ руб.', text)
q2 = re.findall(r'на сумму.*руб.', text)
print(q2)
print(len(q2))
q3 = q2[0]
print(q3)
q1 = q3.replace('на сумму ', '').replace(' руб.', '').replace(' ', '')
print(q1)

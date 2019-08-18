import re
from lxml import html

with open(r"paykeeper.html", encoding="utf-8") as file:
    data = file.read()
payment = {"Фамилия": "",
"Имя": "",
"Фамилия Имя": "",
"Электронная почта": "",
"Наименование услуги": "",
"ID платежа": "",
"Оплаченная сумма": "",
"Кассовый чек 54-ФЗ": "",
"Время проведения": "",
"Номер карты": "",
"Тип карты": "",
"Защита 3-D Secure": "",
"Номер транзакции": "",
"Код авторизации": ""
}
tree = html.fromstring(data)
# print(tree)
# Вот такая строка XPath у меня сработала
# res = tree.xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[5]/tbody/tr/td[2]/table")
tables = tree.xpath('//table[@width="430"]')
# print(f"res={tables}")
for table in tables:
     trs = table.xpath('.//tr')
     # print(f"tr={trs}")
     for td in trs:
         tds = td.xpath('.//td')
         # print(f"tds={tds}")
         text1 = tds[0].text_content()
         text2 = tds[1].text_content()
         #print(f"text={text1}|{text2}")
         print(f'"{text1}": "",')
         payment[text1]=text2;
link = tree.xpath('//a[text()="Ссылка на чек"]/@href')
#print(link[0])
payment["Кассовый чек 54-ФЗ"]=link[0]
payment["Фамилия Имя"]=payment["Фамилия Имя"].strip()
payment["Оплаченная сумма"]=payment["Оплаченная сумма"].split(".")[0].replace(" ","")
fio = payment["Фамилия Имя"].split(" ")
payment["Фамилия"]=fio[0]
payment["Имя"]=''.join(fio[1:])
print(payment)

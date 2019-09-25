import datetime
import requests
import re
from lxml import html


def get_clear_payment():
    payment_zero = {
        "payment_id": "",
        "participant_id": "",
        "number_of_days": 30,
        "deadline": "",
        "Фамилия": "",
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
        "Код авторизации": "",
        "Платежная система": 0
    }
    return payment_zero


def payment_normalization(payment):
    """Bring payment to standard form.
    Sum = to Integer
    Last Name, First Name, LN+FN = to UPPER
    Email = to LOVER
    """
    payment["Оплаченная сумма"] = int(payment["Оплаченная сумма"])
    payment["Фамилия"] = payment["Фамилия"].upper()
    payment["Имя"] = payment["Имя"].upper()
    payment["Фамилия Имя"] = payment["Фамилия Имя"].upper()
    payment["Электронная почта"] = payment["Электронная почта"].lower()
    return payment


def payment_computation(payment):
    # По сумме оплаты вычислить за сколько месяцев оплачено
    if payment["Оплаченная сумма"] > 10000:
        payment["number_of_days"] = 180
    elif payment["Оплаченная сумма"] > 5000:  # от 5000 до 10000
        payment["number_of_days"] = 90
    # Вычисляем до какой даты произведена оплата
    if isinstance(payment["Время проведения"], datetime.datetime):
        payment["deadline"] = payment["Время проведения"] + datetime.timedelta(days=payment["number_of_days"])
    return payment


def parse_getcourse_html(body_html):
    # TODO: Реализовать аутентификацию на getcourse, чтобы мочь пройти по ссылке в письме на страницу платежа.
    #       Это можно обойти через вебхуки
    #       А пока написал на форум
    #       https://stackoverflow.com/questions/57555807/how-to-authenticate-to-this-site-with-python
    payment = get_clear_payment()
    tree = html.fromstring(body_html)
    td = tree.xpath('//div/table/tr[1]/td[2]')
    # print(td)
    # print("=" * 45)
    # print(td[0].text_content())
    # print("=" * 45)
    raw_text = td[0].text_content().splitlines()
    order_list = ""
    for i, line in enumerate(raw_text):
        line = line.strip()
        if len(line) != 0:
            # print(line)
            if line.startswith('Поступила оплата'):
                payment["ID платежа"] = re.findall(r'\d{4}', line)[0]
                payment["Оплаченная сумма"] = re.findall(r'\d+ \d+', line)[0].replace(' ', '')
                # print('1')
                # result = re.findall(r'\d{4}', line)
                # print(result[0])
                # result2 = re.findall(r'\d+ \d+', line)
                # print(result2[0])
            elif line.startswith('Страница заказ:'):
                payment["Кассовый чек 54-ФЗ"] = line.split(' ')[2].strip()
                # link = line.split(' ')[2].strip()
                # print(link)
            elif line.startswith('Клиент:'):
                payment["Фамилия Имя"] = line.split(':')[1].strip()
                # print(f'1:{payment["Фамилия Имя"]}')
                # client = line.split(':')[1].strip()
                # print(client)
            elif line.startswith('Состав заказа:'):
                # print(f'4={i}')
                p = i
            elif i > p:
                order_list = order_list + ' ' + line
    order_list = order_list.strip()
    payment["Наименование услуги"] = order_list
    # print(order_list)
    # print("=" * 45)
    fio = payment["Фамилия Имя"].split(" ")
    # print(f'2:{fio}')
    payment["Имя"] = fio[0]
    payment["Фамилия"] = ''.join(fio[1:])
    # В письме идет сначало имя а потом фамилия
    payment["Фамилия Имя"] = payment["Фамилия"] + " " + payment["Имя"]
    # print(f'3:{payment["Фамилия"]}')
    # print(f'4:{payment["Имя"]}')
    # print(f'5:{payment["Фамилия Имя"]}')
    # У GetCourse в письме дата не указана, поэтому ставлю текущую
    # TODO Получать дату оплаты для GetCourse по дате и времени самого письма
    payment["Время проведения"] = datetime.datetime.now()
    payment["Платежная система"] = 1
    payment = payment_normalization(payment)
    payment = payment_computation(payment)
    # print(payment)
    return payment


def parse_paykeeper_html(body_html):
    payment = get_clear_payment()
    tree = html.fromstring(body_html)
    # print(tree)
    # Вот такая строка XPath у меня сработала
    # res =
    # tree.xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td/table/tbody/tr/td/table[5]/tbody/tr/td[2]/table")
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
            # print(f"text={text1}|{text2}")
            # print(f'"{text1}": "",')
            payment[text1] = text2
            # print(payment)
    link = tree.xpath('//a[text()="Ссылка на чек"]/@href')
    # print(link[0])
    payment["Кассовый чек 54-ФЗ"] = link[0]
    payment["Фамилия Имя"] = payment["Фамилия Имя"].strip()
    payment["Оплаченная сумма"] = payment["Оплаченная сумма"].split(".")[0].replace(" ", "")
    fio = payment["Фамилия Имя"].split(" ")
    payment["Фамилия"] = fio[0]
    payment["Имя"] = ''.join(fio[1:])
    payment["Время проведения"] = datetime.datetime.strptime(payment["Время проведения"], '%Y-%m-%d %H:%M:%S')
    payment["Платежная система"] = 2
    payment = payment_normalization(payment)
    payment = payment_computation(payment)
    # print(payment)
    return payment


# FOR TEST
def parse_getcourse_html_test(body_html):
    with open(r"getcourse.html", encoding="utf-8") as file:
        data = file.read()
    tree = html.fromstring(data)
    # tree = html.fromstring(body_html)
    link = tree.xpath('//a/@href')[0]
    print(link)
    # establishing session
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'referer': 'https://givinschoolru.getcourse.ru/cms/system/login?required=true'})
    s.auth = ('ministrbob777@gmail.com', 'Jager777Z7')
    payload = {
        "email": 'ministrbob777@gmail.com',
        "password": 'Jager777Z7'
    }
    r = s.post(r"https://givinschoolru.getcourse.ru/cms/system/login?required=true", data=payload)
    print(r)
    r = s.get(
        r"http://givinschoolru.getcourse.ru/g/2709590526/446cb0e2?v=Y1DOxkjM4EzLkl2LlRXYkBXdvwWYlR2Ls9mc052bj9yclxWYz9Sdy5SZzJXdvNGdldmL1JHbv9GajNnbpZXan9yL6MHc0RHa")
    # r = s.get(link)

    # r = requests.get(link, headers=headers)
    print(r)
    print(r.text)
    # print(r.content.decode())
    tree2 = html.fromstring(r.content.decode())
    h1 = tree2.xpath('//h1')
    # print(h1)
    # print(h1.text_content())


if __name__ == "__main__":
    parse_getcourse_html("aaaa")

import datetime
import requests
import re
import PASSWORDS
import traceback
import time
from lxml import html
from utils import is_eng
from utils import is_rus
from alert_to_mail import send_mail
from selenium import webdriver


def get_clear_payment():
    payment_zero = {
        "task_uuid": "",
        "participant_id": "",
        "number_of_days": 30,
        "deadline": "",
        "fio_lang": "RUS",
        "participant_type": "",
        "Фамилия": "",
        "Имя": "",
        "Фамилия Имя": "",
        "Электронная почта": "",
        "telegram": "",
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
    payment_normalization2(payment)
    if is_rus(payment["Фамилия Имя"]):
        payment["fio_lang"] = "RUS"
    elif is_eng(payment["Фамилия Имя"]):
        payment["fio_lang"] = "ENG"
    else:
        raise Exception(f"ERROR: Неизвестный язык ФИО: {payment['Фамилия Имя']}")


def payment_normalization2(payment):
    payment["Электронная почта"] = payment["Электронная почта"].lower()
    payment["telegram"] = payment["telegram"].lower()


def payment_computation(payment):
    # По сумме оплаты вычислить за сколько месяцев оплачено
    if payment["Оплаченная сумма"] > 10000:
        payment["number_of_days"] = 180
    elif payment["Оплаченная сумма"] > 5000:  # от 5000 до 10000
        payment["number_of_days"] = 90
    # Вычисляем до какой даты произведена оплата
    if isinstance(payment["Время проведения"], datetime.datetime):
        payment["deadline"] = payment["Время проведения"] + datetime.timedelta(days=payment["number_of_days"])


def parse_getcourse_html(body_html, logger):
    logger.info("Парсинг parse_paykeeper_html")
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
                # print(line)
                # Так ищет любые суммы и <1000 тоже
                payment["Оплаченная сумма"] = re.findall(r'на сумму.*руб.', line)[0] \
                    .replace('на сумму ', '').replace('руб.', '').replace(' ', '')
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
    # У некоторых фамили и имена сложные = несколько слов через пробел, поэтому пробел заменяю на подчёркивание
    payment["Фамилия"] = ' '.join(fio[1:]).strip()
    # В письме идет сначало имя а потом фамилия
    payment["Фамилия Имя"] = payment["Фамилия"] + " " + payment["Имя"]
    # print(f'3:{payment["Фамилия"]}')
    # print(f'4:{payment["Имя"]}')
    # print(f'5:{payment["Фамилия Имя"]}')
    # У GetCourse в письме дата не указана, поэтому ставлю текущую
    # TODO Получать дату оплаты для GetCourse по дате и времени самого письма
    payment["Время проведения"] = datetime.datetime.now()
    payment["Платежная система"] = 1
    payment_normalization(payment)
    payment_computation(payment)
    # print(payment)
    return payment


def parse_paykeeper_html(body_html, logger):
    logger.info("Парсинг parse_paykeeper_html")
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
    # У некоторых фамили и имена сложные = несколько слов через пробел, поэтому пробел заменяю на подчёркивание
    payment["Имя"] = ' '.join(fio[1:]).strip()
    payment["Время проведения"] = datetime.datetime.strptime(payment["Время проведения"], '%Y-%m-%d %H:%M:%S')
    payment["Платежная система"] = 2
    payment_normalization(payment)
    payment_computation(payment)
    # print(payment)
    return payment


def parse_getcourse_page(link, payment, logger):
    """
    Парсинг страницы заказа GetCourse и получение email и telegram.
    Пытаемся получить email и Telegram, если ошибка просто пишем в лог и идём дальше.
    Пример вызова: parse_getcourse_page(payment["Кассовый чек 54-ФЗ"], payment, logger)
    :param link: Ссылка на страницу заказа GetCourse
    :param payment: Теущий платёж
    :param logger: Текущий логгер
    :return:
    """
    """
    Алексей Сутов, [05.10.19 13:17]
    тебе на питоне надо сделать Login, сохранить все куки и потом уже спрашивать
    Алексей Сутов, [05.10.19 13:17]
    там php session id + csrf token
    Алексей Сутов, [05.10.19 13:17]
    причём csrf они вроде не проверяют, раз из постмана могу всё грузить
    url = "https://givinschoolru.getcourse.ru/cms/system/login"
    querystring = {"required": "true"}
    payload = "action=processXdget&xdgetId=99945&params%5Baction%5D=login&params%5Bemail%5D=asutov%40outlook.com&params%5Bpassword%5D=password123"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Postman-Token': "86a39678-b2c1-4169-8fad-6444b53ed97a"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)
    """
    try:
        browser = webdriver.Chrome()
        # browser = webdriver.Chrome(r'chromedriver.exe')
        # browser = webdriver.Chrome(r'c:\Windows\System32\chromedriver.exe')
        # browser = webdriver.Chrome(r'c:\Users\MinistrBob\.wdm\drivers\chromedriver\79.0.3945.36\win32\chromedriver.exe')
        browser.get(PASSWORDS.logins['getcourse_login_page'])
        input_login = browser.find_element_by_css_selector("input.form-control.form-field-email")
        input_login.send_keys(PASSWORDS.logins['getcourse_login'])
        input_password = browser.find_element_by_css_selector("input.form-control.form-field-password")
        input_password.send_keys(PASSWORDS.logins['getcourse_password'])
        button = browser.find_element_by_css_selector(".float-row > .btn-success")
        button.click()
        time.sleep(10)
        link_id = link.rsplit("/", 1)
        link = "https://givinschoolru.getcourse.ru/sales/control/deal/update/id/" + link_id[1]
        browser.get(link)
        time.sleep(10)
        email_element = browser.find_element_by_css_selector("div.user-email")
        email = email_element.text
        if len(email) < 0:
            logger.warning(f"PARSING: Не нашел email на странице заказа - {link}")
        else:
            # print(f"email={email}")
            payment["Электронная почта"] = email
            logger.info(f"PARSING: email={email}")
        telegram_elements = browser.find_elements_by_css_selector(".text-block>div[style]")
        text = ""
        for telegram_element in telegram_elements:
            text += telegram_element.text
        # print(text)
        logger.info(f"PARSING: text={text}")
        # Сначала ищем нормальное написание @xxxx
        mask = r'@\w*'
        result = re.search(mask, text)
        if result is None:
            # Иногда указывают ссылку на страницу telegram
            mask = r'https://t.me/\w*'
            result = re.search(mask, text)
            if result is None:
                # Иногда указывают имя без символа @ (здесь может выбраться некоректное имя)
                mask = r'[a-zA-Z0-9_]+'
                result = re.search(mask, text)
                if result is None:
                    logger.warning(f"PARSING: Не нашел telegram на странице заказа - {link}")
                else:
                    result = result.group(0)
            else:
                result = '@' + result.group(0).rsplit("/", 1)[1]
        else:
            result = result.group(0)
        print(f"telegram={result}")
        payment["telegram"] = result
        logger.info(f"PARSING: telegram={result}")
        # закрываем браузер после всех манипуляций
        browser.quit()
        payment_normalization(payment)
    except Exception as e:
        mail_text = f'Ошибка парсинга страницы заказа GetCourse\n' + traceback.format_exc()
        logger.error(mail_text)
        send_mail(PASSWORDS.logins['admin_emails'], "ERROR PARSING", mail_text, logger)
    finally:
        # закрываем браузер даже в случае ошибки
        browser.quit()


if __name__ == "__main__":
    # parse_getcourse_html("aaaa")
    import logging
    logger = logging.basicConfig(filename='parser.log', level=logging.INFO)
    payment = get_clear_payment()
    parse_getcourse_page("https://givin.school/sales/control/deal/update/id/24611232", payment, logger)
    print(payment)
    payment = get_clear_payment()
    parse_getcourse_page("https://givin.school/sales/control/deal/update/id/24968591", payment, logger)
    print(payment)

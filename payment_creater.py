import requests
import re
import PASSWORDS
import traceback
import time
from datetime import datetime
from datetime import timedelta
from lxml import html
from utils import is_eng
from utils import is_rus
from alert_to_mail import send_mail
from selenium import webdriver


def get_clear_payment():
    payment_zero = {
        "task_uuid": None,
        "participant_id": None,
        "number_of_days": 30,
        "deadline": None,
        "until_date": None,
        "fio_lang": "RUS",
        "participant_type": None,
        "login": None,
        "password": None,
        "auto": True,
        "Фамилия": None,
        "Имя": None,
        "Фамилия Имя": None,
        "Электронная почта": None,
        "telegram": None,
        "Наименование услуги": None,
        "ID платежа": None,
        "Оплаченная сумма": None,
        "Кассовый чек 54-ФЗ": None,
        "Время проведения": None,
        "Номер карты": None,
        "Тип карты": None,
        "Защита 3-D Secure": None,
        "Номер транзакции": None,
        "Код авторизации": None,
        "Платежная система": 0
    }
    return payment_zero


def payment_normalization(payment):
    """Bring payment to standard form.
    Sum = to Integer
    Last Name, First Name, LN+FN = to UPPER
    Email = to LOVER
    """
    if payment["Оплаченная сумма"]:
        payment["Оплаченная сумма"] = int(payment["Оплаченная сумма"])
    else:
        payment["Оплаченная сумма"] = 0
    payment["Фамилия"] = payment["Фамилия"].upper()
    payment["Имя"] = payment["Имя"].upper()
    if not payment["Фамилия Имя"]:
        payment["Фамилия Имя"] = payment["Фамилия"] + " " + payment["Имя"]
    else:
        payment["Фамилия Имя"] = payment["Фамилия Имя"].upper()
    payment_normalization2(payment)
    if is_rus(payment["Фамилия Имя"]):
        payment["fio_lang"] = "RUS"
    elif is_eng(payment["Фамилия Имя"]):
        payment["fio_lang"] = "ENG"
    else:
        raise Exception(f"ERROR: Неизвестный язык ФИО: {payment['Фамилия Имя']}")


def payment_normalization2(payment):
    if payment["Электронная почта"]:
        payment["Электронная почта"] = payment["Электронная почта"].lower()
    if payment["telegram"]:
        payment["telegram"] = payment["telegram"].lower()


def payment_computation(payment):
    # По сумме оплаты вычислить за сколько месяцев оплачено
    if payment["Оплаченная сумма"] < 3980:  # <=1990 >1990 <3980 весь этот промежуток это 30 дней
        payment["number_of_days"] = 30
    elif 3980 <= payment["Оплаченная сумма"] < 5580:
        payment["number_of_days"] = 60
    elif 5580 <= payment["Оплаченная сумма"] < 7440:
        payment["number_of_days"] = 90
    elif 7440 <= payment["Оплаченная сумма"] < 9300:
        payment["number_of_days"] = 120
    elif 9300 <= payment["Оплаченная сумма"] < 10440:
        payment["number_of_days"] = 150
    elif 10440 <= payment["Оплаченная сумма"] < 20280:
        payment["number_of_days"] = 180
    elif payment["Оплаченная сумма"] >= 20280:
        payment["number_of_days"] = 365
    # Вычисляем до какой даты произведена оплата
    if isinstance(payment["Время проведения"], datetime):
        payment["deadline"] = payment["Время проведения"] + timedelta(days=payment["number_of_days"])


def parse_getcourse_html(body_html, logger):
    logger.info(">>>> parse_getcourse_html begin")
    # logger.info("Парсинг parse_getcourse_html")
    logger.debug(f"body_html=\n{body_html}\n")
    payment = get_clear_payment()
    tree = html.fromstring(body_html)
    td = tree.xpath('//div/table/tr[1]/td[2]')
    # print(td)
    # print("=" * 45)
    # print(td[0].text_content())
    # print("=" * 45)
    raw_text = td[0].text_content().splitlines()
    order_list = ""
    p = 0
    for i, line in enumerate(raw_text):
        line = line.strip()
        if len(line) != 0:
            # print(line)
            logger.debug(f"line={line}")
            if line.startswith('Поступила оплата'):
                payment["ID платежа"] = re.findall(r'\d{4}', line)[0]
                logger.debug(f'ID платежа={payment["ID платежа"]}')
                # print(line)
                # Так ищет любые суммы и <1000 тоже
                if len(re.findall(r'на сумму.*руб.', line)) > 0:
                    payment["Оплаченная сумма"] = re.findall(r'на сумму.*руб.', line)[0] \
                        .replace('на сумму ', '').replace('руб.', '').split('.')[0].replace(' ', '')
                    logger.debug(f'Оплаченная сумма={payment["Оплаченная сумма"]}')
                else:
                    payment["Оплаченная сумма"] = "0"
                    logger.warning(f'Оплаченная сумма не в рублях = {line}')
                # print('1')
                # result = re.findall(r'\d{4}', line)
                # print(result[0])
                # result2 = re.findall(r'\d+ \d+', line)
                # print(result2[0])
            elif line.startswith('Страница заказ:') or line.startswith('Страница заказа:'):
                payment["Кассовый чек 54-ФЗ"] = line.split(' ')[2].strip()
                logger.debug(f'Кассовый чек 54-ФЗ={payment["Кассовый чек 54-ФЗ"]}')
                # link = line.split(' ')[2].strip()
                # print(link)
            elif line.startswith('Клиент:'):
                payment["Фамилия Имя"] = line.split(':')[1].strip()
                logger.debug(f'Фамилия Имя={payment["Фамилия Имя"]}')
                # print(f'1:{payment["Фамилия Имя"]}')
                # client = line.split(':')[1].strip()
                # print(client)
            elif line.startswith('Состав заказа:'):
                # print(f'4={i}')
                p = i
                logger.debug(f'Состав заказа1: p={p} i={i}')
            elif i > p:
                logger.debug(f'Состав заказа2: p={p} i={i}')
                order_list = order_list + ' ' + line
                logger.debug(f'order_list={order_list}')
    order_list = order_list.strip()
    payment["Наименование услуги"] = order_list
    logger.debug(f'Наименование услуги={order_list}')
    # print(order_list)
    # print("=" * 45)
    fio = payment["Фамилия Имя"].split(" ")
    logger.debug(f'fio={fio}')
    # print(f'2:{fio}')
    payment["Имя"] = fio[0]
    logger.debug(f'Имя={payment["Имя"]}')
    # У некоторых фамили и имена сложные = несколько слов через пробел, поэтому пробел заменяю на подчёркивание
    payment["Фамилия"] = ' '.join(fio[1:]).strip()
    logger.debug(f'Фамилия={payment["Фамилия"]}')
    # В письме идет сначало имя а потом фамилия
    payment["Фамилия Имя"] = payment["Фамилия"] + " " + payment["Имя"]
    logger.debug(f'Фамилия Имя={payment["Фамилия Имя"]}')
    # print(f'3:{payment["Фамилия"]}')
    # print(f'4:{payment["Имя"]}')
    # print(f'5:{payment["Фамилия Имя"]}')
    # У GetCourse в письме дата не указана, поэтому ставлю текущую
    # Получать дату оплаты для GetCourse по дате и времени самого письма
    # https://github.com/DevGivinSchool/GivinToolsPython/projects/1#card-41172417

    payment["Время проведения"] = datetime.now()
    payment["Платежная система"] = 1
    payment_normalization(payment)
    payment_computation(payment)
    logger.info(f'payment after parsing\n{payment}')
    logger.info(">>>> parse_getcourse_html end")
    return payment


def parse_paykeeper_html(body_html, logger):
    logger.info(">>>> parse_paykeeper_html begin")
    logger.debug(f"body_html=\n{body_html}\n")
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
    payment["Время проведения"] = datetime.strptime(payment["Время проведения"], '%Y-%m-%d %H:%M:%S')
    payment["Платежная система"] = 2
    payment_normalization(payment)
    payment_computation(payment)
    logger.info(f'payment after parsing\n{payment}')
    logger.info(">>>> parse_paykeeper_html end")
    return payment


def parse_getcourse_page(link, payment, logger):
    logger.info(">>>> parse_getcourse_page start")
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
        logger.debug(f"headless={PASSWORDS.settings['headless']}")
        logger.debug(f"chromedriver_path={PASSWORDS.settings['chromedriver_path']}")
        if PASSWORDS.settings['headless']:
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--headless")
            browser = webdriver.Chrome(PASSWORDS.settings['chromedriver_path'], options=chromeOptions)
        else:
            browser = webdriver.Chrome(PASSWORDS.settings['chromedriver_path'])
        logger.debug(f"browser={browser}")
        # Вход в GetCourse иначе страница заказа будет недоступна
        logger.debug(f"Try login to GetCourse")
        browser.get(PASSWORDS.settings['getcourse_login_page'])
        input_login = browser.find_element_by_css_selector("input.form-control.form-field-email")
        input_login.send_keys(PASSWORDS.settings['getcourse_login'])
        input_password = browser.find_element_by_css_selector("input.form-control.form-field-password")
        input_password.send_keys(PASSWORDS.settings['getcourse_password'])
        button = browser.find_element_by_css_selector(".float-row > .btn-success")
        button.click()
        time.sleep(10)
        # Выделить из ссылки заказа ID и открыть страницу заказа (ссылка которая в письме не открывается)
        logger.debug(f"Выделить из ссылки заказа ID и открыть страницу заказа")
        link_id = link.rsplit("/", 1)
        link = "https://givinschoolru.getcourse.ru/sales/control/deal/update/id/" + link_id[1]
        logger.debug(f"link={link}")
        browser.get(link)
        time.sleep(10)
        # Поиск email на странице заказа
        logger.debug(f"Поиск email на странице заказа")
        email_element = browser.find_element_by_css_selector("div.user-email")
        logger.debug(f"email_element.text={email_element.text}")
        email = email_element.text
        if len(email) < 0:
            logger.warning(f"PARSING: Не нашел email на странице заказа - {link}")
        else:
            # print(f"email={email}")
            payment["Электронная почта"] = email
            logger.info(f"PARSING: email={email}")
        # Поиск telegram на странице заказа
        # telegram вариант 2 (только первый div может содержать telegram)
        logger.debug(f"Поиск telegram на странице заказа. Вариант 2")
        telegram_elements = browser.find_elements_by_xpath(
            "//*[contains(text(), 'Ник телеграмм')]/following-sibling::div")
        result = None
        if len(telegram_elements) == 0:
            logger.info(f"PARSING: На странице нет элемента 'Ник телеграмм'")
        else:
            logger.debug(f"telegram_elements[0].text={telegram_elements[0].text}")
            result = get_telegram_from_text(telegram_elements[0].text, logger)
        if not result:
            # telegram вариант 1 (здесь несколько равнозначных блоков из них выделяется телеграм, можно по идее брать
            # только второй блок)
            logger.debug(f"Поиск telegram на странице заказа. Вариант 1")
            telegram_elements = browser.find_elements_by_css_selector(".text-block>div[style]")
            if len(telegram_elements) > 0:
                text = ""
                for telegram_element in telegram_elements:
                    text += telegram_element.text
                result = get_telegram_from_text(text, logger)
        if result:
            print(f"telegram={result}")
            payment["telegram"] = result
            logger.info(f"PARSING: telegram={result}")
        else:
            logger.warning(f"PARSING: Не нашел telegram на странице заказа - {link}")
        # закрываем браузер после всех манипуляций
        logger.debug(f"закрываем браузер после всех манипуляций")
        browser.quit()
        logger.debug(f"payment_normalization(payment)")
        payment_normalization(payment)
    except:
        mail_text = f'Ошибка парсинга страницы заказа GetCourse\n' + traceback.format_exc()
        logger.error(mail_text)
        send_mail(PASSWORDS.settings['admin_emails'], "ERROR PARSING", mail_text, logger)
    finally:
        # закрываем браузер даже в случае ошибки
        browser.quit()
    logger.info(">>>> parse_getcourse_page end")


def get_telegram_from_text(text, logger):
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
                result=""
            else:
                result = "@" + result.group(0)
        else:
            result = '@' + result.group(0).rsplit("/", 1)[1]
    else:
        result = result.group(0)
    return result


if __name__ == "__main__":
    import custom_logger
    import os

    program_file = os.path.realpath(__file__)
    logger = custom_logger.get_logger(program_file=program_file)

    # parse_getcourse_html("aaaa")

    # telegram вариант 1
    # payment = get_clear_payment()
    # parse_getcourse_page("https://givin.school/sales/control/deal/update/id/24611232", payment, logger)
    # print(payment)
    # payment = get_clear_payment()
    # parse_getcourse_page("https://givin.school/sales/control/deal/update/id/24968591", payment, logger)
    # print(payment)
    # telegram вариант 1
    # payment = get_clear_payment()
    # parse_getcourse_page("https://givin.school/sales/control/deal/update/id/34128218", payment, logger)
    # print(payment)
    # result = get_telegram_from_text(telegram_elements[0].text, logger)
    # IndexError: list index out of range
    # payment = get_clear_payment()
    # parse_getcourse_page("https://givinschoolru.getcourse.ru/sales/control/deal/update/id/43670994", payment, logger)
    # print(payment)
    payment = get_clear_payment()
    parse_getcourse_page("https://givin.school/sales/control/deal/update/id/55563843", payment, logger)
    print(payment)

#!/home/robot/MyGit/GivinToolsPython/venv/bin/python3.8
import sys
import traceback
import xlsxwriter
import os
import PASSWORDS
import gtp_participant_block
from DBPostgres import DBPostgres
from Log import Log
from log_config import log_dir, log_level
from alert_to_mail import send_mail
from datetime import datetime

# Текущая дата для имени лог файла (без %S)
now = datetime.now().strftime("%Y%m%d%H%M")
logger = Log.setup_logger('__main__', log_dir, f'gtp_daily_works_{now}.log',
                          log_level)
logger.info('START gtp_daily_works')


def block_participants(dbconnect):
    """
    Блокировка участников у которых оплата просрочена на 5 дней
    :param dbconnect: Соединение с БД
    :return:
    """
    logger.info("Блокировка участников у которых оплата просрочена на 5 дней")
    # Список участников подлежащих блокировке
    sql_text = """SELECT 
--current_date,
until_date - current_date as "INTERVAL2",
deadline - current_date as "INTERVAL",
--last_name, 
--first_name,
fio, 
email, 
telegram,
payment_date, 
number_of_days, 
deadline, 
until_date,
--,comment
id
FROM public.participants
WHERE type in ('P', 'N')
and (
    ((deadline - current_date = -5 and until_date is NULL) or (until_date - current_date = -5 and until_date is not NULL))
)
order by last_name"""

    values_tuple = (None,)
    records = dbconnect.execute_select(sql_text, values_tuple)
    # (None, 7, 'АЛААА', 'anxxxxx@mail.ru', datetime.date(2019, 12, 31), None)
    # (None, 7, 'БАРААААА', 'ИРАААА', 'barxxxx.xxx@inbox.ru', '@irinabar6', datetime.date(2019, 12, 8), 30, datetime.date(2020, 1, 7), None)
    # (None, 7, 'БАРААААА ИРАААА', 'barxxxx.xxx@inbox.ru', '@irinabar6', datetime.date(2019, 12, 8), 30, datetime.date(2020, 1, 7), None)
    intervals = {3: "3 дня", 7: "7 дней"}

    for p in records:
        # Определяем что используется Срок оплаты или отсрочка
        if p[7] is None:
            until_date = p[8]
        else:
            until_date = p[7]

        try:
            gtp_participant_block.block_one_participant(p[9], dbconnect, logger)

            mail_text = f"""Здравствуйте, {p[2].title()}!  
    
    Наша автоматическая система заблокировала вашу учётную запись для Друзей Школы (ДШ),
    потому что вы {p[5].strftime("%d.%m.%Y")} оплатили период {p[6]} дней Друзей Школы (ДШ) 
    и ваша оплата просрочена на 5 дней.
    Система предупреждала вас за 3 и 7 дней до срока, письмом на email - {p[3]}.
    Для разблокировки достаточно просто оплатить ДШ.
    Если же вы больше не хотите участвовать в ДШ - система больше не будет вас беспокоить.
    
    Вы можете оплатить ДШ через эти платёжные системы (в первых двух вариантах доступен PayPal). Во втором варианте возможна оплата сразу за 3 или 6 месяцев, при этом вы полаете скидки 7% и 13% соответственно:
    1) (+PayPal) https://givinschoolru.getcourse.ru/friends
    2) (+PayPal) https://lp.givinschool.org/dsh
    3) https://givinschoolru.getcourse.ru/paykeeper
    
    Пожалуйста, при оплате, указывайте свои Фамилию, Имя, такие же как и при регистрации.
    В назначение платежа можно написать "друзья школы" или просто "дш".
    
    Ваш email:    {p[3]}
    Ваш telegram: {p[4]}
    
    С благодарностью и сердечным теплом,
    команда Школы Гивина.
        """
            print(mail_text)
            logger.info(mail_text)
            send_mail([p[3]], r"[ШКОЛА ГИВИНА]. Оповещение о блокировке в ДШ", mail_text, logger)
        except:
            send_error(f"DAILY WORKS ERROR: Ошибка при попытке заблокировать участника:\n{p}")
        logger.info('=' * 60)


def participants_notification(dbconnect):
    """
    Уведомление участников о необходимости оплаты
    :param dbconnect: Соединение с БД
    :return:
    """
    logger.info("Уведомление участников о необходимости оплаты")
    # Список участников подлежащих уведомлению
    sql_text = """SELECT
--current_date,
until_date - current_date as "INTERVAL2",
deadline - current_date as "INTERVAL",
--last_name, 
--first_name,
fio, 
email, 
telegram,
payment_date, 
number_of_days, 
deadline, 
until_date
--,comment
FROM public.participants
WHERE type in ('P', 'N')
and (
    ((deadline - current_date = 7 and until_date is NULL) or (until_date - current_date = 7 and until_date is not NULL)) 
    or 
    ((deadline - current_date = 3 and until_date is NULL) or (until_date - current_date = 3 and until_date is not NULL))
)
order by last_name"""

    values_tuple = (None,)
    records = dbconnect.execute_select(sql_text, values_tuple)
    # (None, 7, 'АЛААА', 'anxxxxx@mail.ru', datetime.date(2019, 12, 31), None)
    # (None, 7, 'БАРААААА', 'ИРАААА', 'barxxxx.xxx@inbox.ru', '@irinabar6', datetime.date(2019, 12, 8), 30, datetime.date(2020, 1, 7), None)
    # (None, 7, 'БАРААААА ИРАААА', 'barxxxx.xxx@inbox.ru', '@irinabar6', datetime.date(2019, 12, 8), 30, datetime.date(2020, 1, 7), None)
    intervals = {3: "3 дня", 7: "7 дней"}

    for p in records:
        # Интервал высчитывается по двум полям until_date и deadline. Здесь определяется какой из них используется.
        if p[0] is None:
            interval = intervals[p[1]]
        else:
            interval = intervals[p[0]]
        # Определяем что используется Срок оплаты или отсрочка
        if p[7] is None:
            until_date = p[8]
        else:
            until_date = p[7]
        mail_text = f"""Здравствуйте, {p[2].title()}!  

Напоминаем вам о том, что вы {p[5].strftime("%d.%m.%Y")} оплатили период {p[6]} дней Друзей Школы (ДШ).
{until_date} через {interval} у вас истекает оплаченный период Друзей Школы (ДШ).

Вы можете оплатить ДШ через эти платёжные системы (в первых двух вариантах доступен PayPal). Во втором варианте возможна оплата сразу за 3 или 6 месяцев, при этом вы полаете скидки 7% и 13% соответственно:
1) (+PayPal) https://givinschoolru.getcourse.ru/friends
2) (+PayPal) https://lp.givinschool.org/dsh
3) https://givinschoolru.getcourse.ru/paykeeper

Пожалуйста, при оплате, указывайте свои Фамилию, Имя, такие же как и при регистрации.
В назначение платежа можно написать "друзья школы" или просто "дш".

Ваш email:    {p[3]}
Ваш telegram: {p[4]}

С благодарностью и сердечным теплом,
команда Школы Гивина.
    """
        print(mail_text)
        logger.info(mail_text)
        send_mail([p[3]], r"[ШКОЛА ГИВИНА]. Напоминание об оплате ДШ", mail_text, logger)
        logger.info('=' * 60)


def get_list_debtors(dbconnect):
    """
    Получение списка должников и отправка его менеджерам
    :param dbconnect: Соединение с БД
    :return:
    """
    logger.info("Получение списка долников и отправка его менеджерам")

    # Список должников
    sql_text = """SELECT
id, type,
last_name as "Фамилия", first_name as "Имя", email, telegram,
payment_date "Дата оплаты", number_of_days as "Дней", deadline "Оплачено до",
until_date as "Отсрочка до", comment
FROM public.participants
WHERE type in ('P', 'N')
and ((deadline - CURRENT_TIMESTAMP < INTERVAL '0 days' and until_date is NULL)
or (until_date - CURRENT_TIMESTAMP < INTERVAL '0 days' and until_date is not NULL))
order by last_name"""
    values_tuple = (None,)
    records = dbconnect.execute_select(sql_text, values_tuple)
    # (1126, 'P', 'АБРАМОВА', 'ЕЛЕНА', 'el34513543@gmail.com', '@el414342', datetime.date(2019, 8, 7), 45, datetime.date(2019, 9, 21), datetime.date(2019, 10, 15), None)

    # now_for_file = datetime.now().strftime("%d%m%Y_%H%M")
    now_for_file = datetime.now().strftime("%Y_%m_%d")
    xlsx_file_path = os.path.join(log_dir, f'DEBTORS_{now_for_file}.xlsx')
    table_text = get_excel_table(records, xlsx_file_path)

    now_for_text = datetime.now().strftime("%d.%m.%Y")
    mail_text = f"""Здравствуйте!

Во вложении содержиться список должников на сегодня {now_for_text} в формате xlsx.
Таблица в виде текста:
{table_text}
    
С уважением, ваш робот."""
    print(mail_text)
    logger.info(mail_text)
    send_mail(PASSWORDS.logins['manager_emails'], f"[ШКОЛА ГИВИНА]. Список должников {now_for_text}",
              mail_text, logger, xlsx_file_path)

    # Полный список участников
    sql_text = """SELECT
id, type,
last_name as "Фамилия", first_name as "Имя", email, telegram,
payment_date "Дата оплаты", number_of_days as "Дней", deadline "Оплачено до",
until_date as "Отсрочка до", comment
FROM public.participants
WHERE type in ('P', 'N')
order by last_name"""
    values_tuple = (None,)
    records = dbconnect.execute_select(sql_text, values_tuple)
    # (1126, 'P', 'АБРАМОВА', 'ЕЛЕНА', 'el34513543@gmail.com', '@el414342', datetime.date(2019, 8, 7), 45, datetime.date(2019, 9, 21), datetime.date(2019, 10, 15), None)

    # now_for_file = datetime.now().strftime("%d%m%Y_%H%M")
    now_for_file = datetime.now().strftime("%Y_%m_%d")
    xlsx_file_path = os.path.join(log_dir, f'PARTICIPANTS_{now_for_file}.xlsx')
    table_text = get_excel_table(records, xlsx_file_path)

    now_for_text = datetime.now().strftime("%d.%m.%Y")
    mail_text = f"""Здравствуйте!

Во вложении содержиться полный список участников ДШ на {now_for_text} в формате xlsx.
Таблица в виде текста:
{table_text}

С уважением, ваш робот."""
    print(mail_text)
    logger.info(mail_text)
    send_mail(PASSWORDS.logins['full_list_participants_to_emails'],
              f"[ШКОЛА ГИВИНА]. Полный список участников ДШ на {now_for_text}",
              mail_text, logger, xlsx_file_path)


def get_full_list_participants(dbconnect):
    """
    Получение полного списка участников и отправка его менеджерам
    :param dbconnect: Соединение с БД
    :return:
    """
    logger.info("Получение полного списка участников и отправка его менеджерам")
    # Полный список участников
    sql_text = """SELECT
id, type,
last_name as "Фамилия", first_name as "Имя", email, telegram,
payment_date "Дата оплаты", number_of_days as "Дней", deadline "Оплачено до",
until_date as "Отсрочка до", comment
FROM public.participants
WHERE type in ('P', 'N')
order by last_name"""
    values_tuple = (None,)
    records = dbconnect.execute_select(sql_text, values_tuple)
    # (1126, 'P', 'АБРАМОВА', 'ЕЛЕНА', 'el34513543@gmail.com', '@el414342', datetime.date(2019, 8, 7), 45, datetime.date(2019, 9, 21), datetime.date(2019, 10, 15), None)

    # now_for_file = datetime.now().strftime("%d%m%Y_%H%M")
    now_for_file = datetime.now().strftime("%Y_%m_%d")
    xlsx_file_path = os.path.join(log_dir, f'PARTICIPANTS_{now_for_file}.xlsx')
    table_text = get_excel_table(records, xlsx_file_path)

    now_for_text = datetime.now().strftime("%d.%m.%Y")
    mail_text = f"""Здравствуйте!

Во вложении содержиться полный список участников ДШ на {now_for_text} в формате xlsx.
Таблица в виде текста:
{table_text}

С уважением, ваш робот."""
    print(mail_text)
    logger.info(mail_text)
    send_mail(PASSWORDS.logins['full_list_participants_to_emails'],
              f"[ШКОЛА ГИВИНА]. Полный список участников ДШ на {now_for_text}",
              mail_text, logger, xlsx_file_path)


# Получение списка participants на основе переданного набора данных record из select
def get_excel_table(records, xlsx_file_path):
    workbook = xlsxwriter.Workbook(xlsx_file_path)
    worksheet = workbook.add_worksheet('Список')
    # Запись заголовков столбцов
    heading = workbook.add_format({'bold': True})
    heading.set_align('center')
    heading.set_align('vcenter')
    worksheet.write(0, 0, 'id', heading)
    worksheet.write(0, 1, 'type', heading)
    worksheet.write(0, 2, 'Фамилия', heading)
    worksheet.write(0, 3, 'Имя', heading)
    worksheet.write(0, 4, 'email', heading)
    worksheet.write(0, 5, 'telegram', heading)
    worksheet.write(0, 6, 'Дата оплаты', heading)
    worksheet.write(0, 7, 'Дней', heading)
    worksheet.write(0, 8, 'Оплачено до', heading)
    worksheet.write(0, 9, 'Отсрочка до', heading)
    worksheet.write(0, 10, 'Коментарий', heading)
    table_text = "id | type | Фамилия | Имя | email | telegram | Дата оплаты | Дней | Оплачено до | Отсрочка до | Коментарий\n"
    table = [[2, 4, 7, 3, 5, 8, 11, 4, 11, 11, 10], ]
    # Начинаем со второй строки.
    date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})
    row = 1
    # Формирование таблицы из данных запроса.
    for rec in records:
        col = 0
        for item in rec:
            # print(row, col, item)
            if col == 6 or col == 8 or col == 9:  # Столбцы в формате даты
                if item is None:
                    worksheet.write(row, col, item)
                    table_text += "None"
                else:
                    # item = datetime.strptime(item, '%Y-%m-%d')
                    # print(type(item))
                    worksheet.write_datetime(row, col, item, date_format)
                    table_text += item.strftime("%d.%m.%Y")
            elif col == 10:  # Коментарий может содержать переносы, убираем их
                if item is None:
                    worksheet.write(row, col, item)
                    table_text += str(item)
                else:
                    worksheet.write(row, col, item.replace("\n", " "))
                    table_text += item.replace("\n", " ")
            else:
                worksheet.write(row, col, item)
                table_text += str(item)
            col += 1
            table_text += " | "  # Разделитель столбцов
        row += 1
        table_text += "\n"  # Разделитель строк
    # Установка ширины столбцов
    worksheet.set_column(0, 1, 5)
    worksheet.set_column(2, 5, 20)
    worksheet.set_column(6, 6, 12)
    worksheet.set_column(7, 7, 5)
    worksheet.set_column(8, 9, 12)
    worksheet.set_column(10, 10, 40)
    workbook.close()
    return table_text


def main():
    """
    Основная процедура выполняет:
    1) Уведомление участников о необходимости оплаты.
    2) Получение списка должников и отправление его менеджерам.
    3) Вычищение из БД участников у которых последняя оплата была более года назад.
    4) Удаление писем старше года.
    Все процедуры выполняются независимо, т.е. при падении одной, происходит оповещение администратора и
    выполнение основной процедуры продолжается.
    Соединение с БД критично, поэтому при невозможности соединиться с БД осуществляется выход из приложения.
    :return:
    """
    logger.info("Try connect to DB")
    try:
        dbconnect = DBPostgres(dbname=PASSWORDS.logins['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                               password=PASSWORDS.logins['postgres_password'],
                               host=PASSWORDS.logins['postgres_host'],
                               port=PASSWORDS.logins['postgres_port'], logger=logger)
    except Exception:
        send_error("DAILY WORKS ERROR: Can't connect to DB!!!")
        logger.error("Exit with error")
        sys.exit(1)
    logger.info('#' * 60)
    # Уведомление участников о необходимости оплаты. Здесь падаем при первой же ошибке, т.к. тут скорее всего может
    # быть только проблема с почтой, а это будет для всех.
    try:
        participants_notification(dbconnect)
    except Exception:
        send_error("DAILY WORKS ERROR: participants_notification()")
    logger.info('#' * 60)
    # Блокировка участников у которых оплата просрочена на 5 дней. Здесь проверка на ошибку для каждого конкретного
    # участника.
    block_participants(dbconnect)
    logger.info('#' * 60)
    # Получение списка должников и отправка его менеджерам
    try:
        get_list_debtors(dbconnect)
    except Exception:
        send_error("DAILY WORKS ERROR: get_list_debtors()")
    # Получение полного списка участников и отправка его менеджерам
    try:
        get_full_list_participants(dbconnect)
    except Exception:
        send_error("DAILY WORKS ERROR: get_full_list_participants()")

    # TODO Процедура удаления пользователей у которых последний платёж год назад вместе со всеми их платёжками и письмами

    # TODO Процедура удаления писем из почты старше 1 года
    logger.info('#' * 60)
    logger.info('END gtp_daily_works')


def send_error(subject):
    """
    Отсылает сообщение об ошибке администратору, так же логирует его и выводит в консоль.
    :param subject: Тема письма
    :return:
    """
    subject = subject.upper()
    error_text = f"{subject}:\n" + traceback.format_exc()
    print(error_text)
    logger.error(error_text)
    logger.error(f"Send email to: {PASSWORDS.logins['admin_emails']}")
    send_mail(PASSWORDS.logins['admin_emails'], subject, error_text, logger)


if __name__ == "__main__":
    main()

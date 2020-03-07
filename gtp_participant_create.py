import yandex_mail
import yandex_connect
import Parser
import traceback
import PASSWORDS
import sys
from DBPostgres import DBPostgres
from alert_to_mail import send_mail
from utils import split_str
from utils import get_login


def select_participant(participant_id, database):
    sql_text = 'SELECT * FROM participants where id=%s;'
    values_tuple = (participant_id,)
    rows = database.execute_select(sql_text, values_tuple)
    return rows


def from_list_create_sf_participants(list_fio, database, logger):
    """
    Создание нескольких участников ДШ по списку 
    :param list_fio: 
    :return: 
    """
    # TODO Сделать возможность обрабатывать либо строку Ф+И либо словарь
    logger.info("Начинаю обработку списка")
    for line in list_fio.splitlines():
        payment = Parser.get_clear_payment()
        # Когда копирую из Google Sheets разделитель = Tab
        # Иванов	Иван
        line_ = split_str(line)
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        # ['Иванов', 'Иван']
        payment["Фамилия"] = line_[0]
        payment["Имя"] = line_[1]
        payment["Время проведения"] = datetime.now()
        payment["Платежная система"] = 1
        Parser.payment_normalization(payment)
        Parser.payment_computation(payment)
        try:
            create_sf_participant(payment, database, logger)
        except:
            mail_text = f'Ошибка создания участника\n' + traceback.format_exc()
            logger.error(mail_text)
            send_mail(PASSWORDS.logins['admin_emails'], "ERROR CREATE PARTICIPANT", mail_text, logger)
    logger.info("Обработка списка закончена")


def create_sf_participant(payment, database, logger):
    # This is new participant
    # Participant must have Name, Surname, Email
    logger.info(f"Создание участника:{payment}")
    if payment["Фамилия"] is None or not payment["Фамилия"]:
        logger.error("The participant must have a Surname")
        raise Exception("The participant must have a Surname")
    if payment["Имя"] is None or not payment["Имя"]:
        logger.error("The participant must have a Name")
        raise Exception("The participant must have a Name")
    if payment["Электронная почта"] is None \
            or not payment["Электронная почта"]:
        logger.error("+" * 60)
        logger.error("The participant must have a Email!!!")
        logger.error("+" * 60)
        # raise Exception("The participant must have a Email")

    # Создаём нового пользователя в БД
    logger.info(f"Создаём нового пользователя в БД ({payment['fio_lang']})")
    if payment["fio_lang"] == "RUS":
        sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
        values_tuple = (payment["Фамилия"], payment["Имя"],
                        payment["Фамилия Имя"], payment["Электронная почта"],
                        payment["telegram"], 'N')
    else:
        sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type, last_name_eng, first_name_eng, fio_eng) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        values_tuple = (payment["Фамилия"], payment["Имя"],
                        payment["Фамилия Имя"], payment["Электронная почта"],
                        payment["telegram"], 'N',
                        payment["Фамилия"], payment["Имя"], payment["Фамилия Имя"])
    payment["participant_id"] = database.execute_dml_id(sql_text, values_tuple)
    logger.info(select_participant(payment["participant_id"]))

    # Отмечаем оплату в БД этому участнику
    mark_payment_into_db(participant_type='N')

    # Прикрепить участника к платежу
    sql_text = """UPDATE payments SET participant_id=%s WHERE task_uuid=%s;"""
    values_tuple = (payment["participant_id"], payment["task_uuid"])
    database.execute_dml(sql_text, values_tuple)
    logger.info(select_payment(payment["task_uuid"]))

    try:
        result = yandex_mail.create_yandex_mail(payment["Фамилия"], payment["Имя"], payment["login"], department_id_=4)
        # Отдел 4 = @ДРУЗЬЯ_ШКОЛЫ
    except yandex_connect.YandexConnectExceptionY as e:
        # Если какие-то проблемы при содании почты, то нужно падать. При дублировании почты возможны варианты.
        # print(e.args[0])
        if e.args[0] == 500:
            print(f"Unhandled exception: Такой пользователь уже существует: {payment['login'] + '@givinschool.org'}")
            raise
        else:
            print("ERROR = " + e.__str__())
            raise
    # Для почты стандартный пароль, а это пароль для Zoom
    # TODO Создание zoom
    # TODO Оповещения


if __name__ == '__main__':
    import logging
    from list import list_fio
    from datetime import datetime
    from Log import Log
    from log_config import log_dir, log_level

    now = datetime.now().strftime("%Y%m%d%H%M")
    logger = Log.setup_logger('__main__', log_dir, f'gtp_create_login_{now}.log', logging.DEBUG)
    try:
        logger.info("Try connect to DB")
        database = DBPostgres(dbname=PASSWORDS.logins['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                              password=PASSWORDS.logins['postgres_password'],
                              host=PASSWORDS.logins['postgres_host'],
                              port=PASSWORDS.logins['postgres_port'], logger=logger)
    except Exception:
        # TODO Вынести процедуру опопвещения MAIN ERROR в отдельную процедуру
        error_text = \
            f"MAIN ERROR (Postgres):\n{traceback.format_exc()}"
        print(error_text)
        logger.error(error_text)
        logger.error(f"Send email to: {PASSWORDS.logins['admin_emails']}")
        send_mail(PASSWORDS.logins['admin_emails'], "MAIN ERROR (Postgres)", error_text, logger)
        logger.error("Exit with error")
        sys.exit(1)
    from_list_create_sf_participants(list_fio, logger=logger)

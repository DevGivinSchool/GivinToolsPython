#!/usr/bin/env python3
import sys
import traceback
import PASSWORDS
from DBPostgres import DBPostgres
from alert_to_mail import send_mail
from datetime import datetime
from alert_to_mail import send_error_to_admin


# def send_error(subject):
#     """
#     Отсылает сообщение об ошибке администратору, так же логирует его и выводит в консоль.
#     :param subject: Тема письма
#     :return:
#     """
#     subject = subject.upper()
#     error_text = f"{subject}:\n" + traceback.format_exc()
#     print(error_text)
#     logger.error(error_text)
#     logger.error(f"Send email to: {PASSWORDS.logins['admin_emails']}")
#     send_mail(PASSWORDS.logins['admin_emails'], subject, error_text, logger)


def birthday_alert(dbconnect):
    pass


if __name__ == "__main__":
    """
    Выбираем из БД всех у кого сегодня ДР и шлём оповещение в пару чатов Telegram
    :return:
    """
    import logger
    import os

    program_file = os.path.realpath(__file__)
    logger = logger.get_logger(program_file=program_file)
    logger.info('START gtp_sf_telegram_bot')
    logger.info("Try connect to DB")
    try:
        dbconnect = DBPostgres(dbname=PASSWORDS.logins['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                               password=PASSWORDS.logins['postgres_password'],
                               host=PASSWORDS.logins['postgres_host'],
                               port=PASSWORDS.logins['postgres_port'], logger=logger)
    except Exception:
        send_error_to_admin("ERROR: Can't connect to DB!!!")
        logger.error("Exit with error")
        sys.exit(1)
    logger.info('\n' + '#' * 120)
    # Основная процедура
    try:
        birthday_alert(dbconnect)
    except Exception:
        send_error_to_admin("ERROR: birthday_alert()")
    logger.info('\n' + '#' * 120)

    logger.info('#' * 120)
    logger.info('END gtp_sf_telegram_bot')

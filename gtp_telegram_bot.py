#!/usr/bin/env python3
import sys
import PASSWORDS
import Class_TelegramBot
from Class_DBPostgres import DBPostgres
from alert_to_mail import raise_error


def birthday_alert(dbconnect, logger):
    sql_text = """select last_name, first_name from team_members WHERE
    DATE_PART('day', birthday) = date_part('day', CURRENT_DATE)
AND
    DATE_PART('month', birthday) = date_part('month', CURRENT_DATE)"""
    values_tuple = (None,)
    records = dbconnect.execute_select(sql_text, values_tuple)
    # ('ИВАНОВ', 'ИВАН')
    logger.debug(f"records={records}")
    if records:
        congratulation = """\nПоздравляем сегодня с днём рождения ❤️🤗🎈:\n"""
        for rec in records:
            logger.debug(f"rec={rec}")
            congratulation += f"{rec[0].capitalize()} {rec[1].capitalize()}\n"
        congratulation += "\n"
        logger.debug(f"congratulation={congratulation}")
        tb = Class_TelegramBot(PASSWORDS.settings['telegram_bot_url1'], logger)
        for chat_id in PASSWORDS.settings['telegram_chats_1']:
            logger.info(f"Отправляю сообщение в чат {chat_id}")
            success, result = tb.send_text_message(chat_id, congratulation)
            logger.debug(f"success={success}")
            logger.debug(f"result=\n{result}")
            if not success:
                raise_error(f"Не могу отправить сообщение\n{result}", logger)


if __name__ == "__main__":
    """
    Выбираем из БД всех у кого сегодня ДР и шлём оповещение в пару чатов Telegram
    """
    import custom_logger
    import os

    program_file = os.path.realpath(__file__)
    logger = custom_logger.get_logger(program_file=program_file)
    logger.info('START gtp_birthday_alert')
    logger.info("Try connect to DB")
    try:
        dbconnect = DBPostgres(dbname=PASSWORDS.settings['postgres_dbname'], user=PASSWORDS.settings['postgres_user'],
                               password=PASSWORDS.settings['postgres_password'],
                               host=PASSWORDS.settings['postgres_host'],
                               port=PASSWORDS.settings['postgres_port'], logger=logger)
    except Exception:
        raise_error("ERROR: Can't connect to DB!!!")
        logger.error("Exit with error")
        sys.exit(1)
    logger.info('\n' + '#' * 120)
    # Основная процедура
    try:
        birthday_alert(dbconnect, logger)
    except Exception:
        raise_error("ERROR: gtp_birthday_alert()")
    logger.info('\n' + '#' * 120)

    logger.info('#' * 120)
    logger.info('END gtp_birthday_alert')

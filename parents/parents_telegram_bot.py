#!/usr/bin/env python3
import sys
import parents.parents_PASSWORDS as parents_PASSWORDS
from core.Class_TelegramBot import TelegramBot
from core.Class_DBPostgres import DBPostgres
from core.alert_to_mail import raise_error


def parents_telegram_bot(dbconnect, logger):
    sql_text = """SELECT message_text FROM telegram_messages where message_id=%s;"""
    values_tuple = (int(sys.argv[1]),)
    records = dbconnect.execute_select(sql_text, values_tuple)
    logger.info(f"records=\n{records}")
    logger.info(f"Сообщение:\n{records[0][0]}")
    if records:
        tb = TelegramBot(parents_PASSWORDS.settings['telegram_bot_parents_url'], logger)
        for chat_id in parents_PASSWORDS.settings['telegram_chats']:
            logger.info(f"Отправляю в чат {chat_id}")
            success, result = tb.send_text_message(chat_id, records[0][0])
            logger.info(f"success={success}")
            logger.info(f"result={result}")
            if not success:
                raise_error(f"Не могу отправить сообщение в чат chat_id={chat_id};result={result}", logger)
    else:
        raise_error(f"Не такого сообщения {sys.argv[1]}", logger)


if __name__ == "__main__":
    """
    Бот для проекта Мы Родители. Рассылка заданий по расписанию.
    
    HTTP запрос на получение updates для бота чтобы посмотреть chat_id группы можно посмотерть в parents_PASSWORDS.py
    
    Вручную можно отправить сообщение так (аргумент в командной строке это message_id):
    Windows: 
        cd c:\\Users\\MinistrBob\\.virtualenvs\\GivinToolsPython\\Scripts
        activate
        cd c:\\yGit\\GivinToolsPython\\
        python parents_telegram_bot.py 1
    """
    import custom_logger
    import os

    program_file = os.path.realpath(__file__)
    logger = custom_logger.get_logger(program_file=program_file)
    logger.info('START parents_telegram_bot')
    logger.info("Try connect to DB")
    try:
        dbconnect = DBPostgres(dbname=parents_PASSWORDS.settings['parents_dbname'], user=parents_PASSWORDS.settings['parents_user'],
                               password=parents_PASSWORDS.settings['parents_password'],
                               host=parents_PASSWORDS.settings['parents_host'],
                               port=parents_PASSWORDS.settings['parents_port'], logger=logger)
    except Exception:
        raise_error("ERROR: Can't connect to DB!!!", logger, prog_name="parents_telegram_bot.py")
        logger.error("Exit with error")
        sys.exit(1)
    logger.info('\n' + '#' * 120)
    # Основная процедура
    try:
        parents_telegram_bot(dbconnect, logger)
    except Exception:
        raise_error("ERROR: parents_telegram_bot()", logger, prog_name="parents_telegram_bot.py")
    logger.info('\n' + '#' * 120)
    logger.info('END parents_telegram_bot')

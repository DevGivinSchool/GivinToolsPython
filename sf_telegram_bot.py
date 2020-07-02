import PASSWORDS
import sys
from Class_TelegramBot import TelegramBot
from Class_DBPostgres import DBPostgres
from alert_to_mail import raise_error, get_participant_notification_text


def mark_telegram_update_id(telegram_update_id_, logger_):
    """
    Зафиксировать telegram_update_id + 1 в БД
    :param telegram_update_id_: Текущий update
    :param logger_: логгер
    """
    sql_text = f"UPDATE settings SET value=%s where key='telegram_update_id' RETURNING key;"
    values_tuple = (telegram_update_id_ + 1,)
    id_ = dbconnect.execute_dml_id(sql_text, values_tuple)
    logger_.debug(f"key={id_}")
    if not id_:
        raise_error("Не могу обновить telegram_update_id", logger_)


if __name__ == '__main__':
    import custom_logger
    import os

    logger = custom_logger.get_logger(program_file=os.path.realpath(__file__))
    logger.info("Try connect to DB")
    try:
        dbconnect = DBPostgres(dbname=PASSWORDS.settings['postgres_dbname'], user=PASSWORDS.settings['postgres_user'],
                               password=PASSWORDS.settings['postgres_password'],
                               host=PASSWORDS.settings['postgres_host'],
                               port=PASSWORDS.settings['postgres_port'], logger=logger)
    except Exception:
        raise_error("Can't connect to DB!!!", logger, prog_name="sf_telegram_bot.py")
        sys.exit(1)
    # logger.info('\n' + '#' * 120)
    # Получить update_id из БД
    rows = dbconnect.execute_select(f"select value from settings where key='telegram_update_id';", None)
    logger.debug(f"rows={rows}")
    if not rows:
        raise_error("Select для telegram_update_id ничего не возвращает", logger, prog_name="sf_telegram_bot.py")
    try:
        telegram_update_id = int(rows[0][0])
    except:
        raise_error("Не могу получить telegram_update_id из БД", logger, prog_name="sf_telegram_bot.py")
    logger.debug(f"telegram_update_id={telegram_update_id}")
    tb = TelegramBot(PASSWORDS.settings['telegram_bot_url2'], logger)
    logger.info("Get updates")
    success, updates = tb.get_text_updates(telegram_update_id)
    logger.debug(f"success={success}")
    logger.debug(f"updates=\n{updates}")
    if not success:
        raise_error(f"Не могу получить updates\n{updates}", logger, prog_name="sf_telegram_bot.py")
    for update in updates['result']:
        try:
            telegram_update_id = int(update['update_id'])
        except:
            raise_error("Не могу получить telegram_update_id из update", logger, prog_name="sf_telegram_bot.py")
        logger.info(f"Processing telegram_update_id={telegram_update_id}")
        try:
            chat_id = update['message']['chat']['id']
        except:
            raise_error("Не могу получить chat_id", logger, prog_name="sf_telegram_bot.py")
        logger.debug(f"chat_id={chat_id}")
        if chat_id > 0:
            try:
                username = f"@{update['message']['chat']['username'].lower()}"
            except:
                raise_error("Не могу получить username", logger, prog_name="sf_telegram_bot.py")
            logger.debug(f"username={username}")
            person = dbconnect.find_participant_by_telegram_username(username)
            logger.debug(person)
            if person is None:
                # Ничего не нашлось
                logger.debug(f"Нет участника с таким telegram username={username}")
                mark_telegram_update_id(telegram_update_id, logger)
            else:
                if person['telegram_id'] is None:
                    # Это новый пользователь, ему нужно отправить логин
                    message = get_participant_notification_text(person['last_name'],
                                                                person['first_name'],
                                                                person['login'],
                                                                person['password'])
                    logger.debug(f"message=\n{message}")
                    logger.info("Отправляю сообщение в Telegram новому участнику")
                    success, result = tb.send_text_message(chat_id, message)
                    logger.debug(f"success={success}")
                    logger.debug(f"result=\n{result}")
                    if not success:
                        raise_error(f"Не могу отправить сообщение\n{result}", logger, prog_name="sf_telegram_bot.py")
                    # Если да - отметить в БД:
                    # 1) внести telegram_id в participants
                    sql_text = f"UPDATE participants SET telegram_id=%s where id=%s RETURNING id;"
                    values_tuple = (chat_id, person['id'])
                    id_ = dbconnect.execute_dml_id(sql_text, values_tuple)
                    logger.debug(f"id_={id_}")
                    if not id_:
                        raise_error(f"Не могу обновить telegram_id={person['telegram_id']} для участника id={person['id']}", logger, prog_name="sf_telegram_bot.py")
                    mark_telegram_update_id(telegram_update_id, logger)
                    logger.info('\n' + '#' * 120)
                else:
                    logger.info(f"Ничего не отправляю, это старый участник telegram_id={person['telegram_id']}")
                    mark_telegram_update_id(telegram_update_id, logger)

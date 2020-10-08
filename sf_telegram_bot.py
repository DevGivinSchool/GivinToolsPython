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
    sql_text = f"UPDATE settings SET value=%s, update_date=NOW() where key='telegram_update_id' RETURNING key;"
    values_tuple = (telegram_update_id_ + 1,)
    id_ = dbconnect.execute_dml_id(sql_text, values_tuple)
    logger_.info(f"key={id_}")
    if not id_:
        raise_error("Не могу обновить telegram_update_id", logger_)


def send_message(tb_, chat_id_, message_, logger_):
    global success
    logger_.info("Отправляю сообщение в Telegram новому участнику")
    success, result = tb_.send_text_message(chat_id_, message_)
    logger_.info(f"success={success}")
    logger_.info(f"result=\n{result}")
    if not success:
        raise_error(f"Не могу отправить сообщение\n{result}", logger_, prog_name="sf_telegram_bot.py")


if __name__ == '__main__':
    """ Логика работы. Оповещение нужно слать только тем кто оплатил (просто добавить себе бота не достаточно)
    Если участник оплатил, но не добавил себе бота, значит он получает только оповещение по email. 
    Никаких даже попыток отправить что-то в telegram при регистрации нового участника не делается.
    Добавил ли себе участник бота проверяется только в этом скрипте. 
    Идём по сообщениям полученных ботом и сравнимаем telegram username с тем что в participants.
    Если IF участник находиться в participants - значит он оплатил и ему можно отправить сообщение.
    Иначе ELSE - участник добавил себе бота но пока не оплатил, заносим его в список проверки telegram_bot_added.
    Отдельно обрабатываем список проверки, если пользователь находиться в participants = оплатил = оповещение.
    Записи в списке проверки храняться 14 дней.
    """
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
    logger.info(f"rows={rows}")
    if not rows:
        raise_error("Select для telegram_update_id ничего не возвращает", logger, prog_name="sf_telegram_bot.py")
    try:
        telegram_update_id = int(rows[0][0])
    except:
        raise_error("Не могу получить telegram_update_id из БД", logger, prog_name="sf_telegram_bot.py")
    logger.info(f"telegram_update_id={telegram_update_id}")
    tb = TelegramBot(PASSWORDS.settings['telegram_bot_url2'], logger)
    logger.info("Get updates")
    success, updates = tb.get_text_updates(telegram_update_id)
    logger.info(f"success={success}")
    logger.info(f"updates={updates}")
    if not success:
        raise_error(f"Не могу получить updates={updates}", logger, prog_name="sf_telegram_bot.py")
    # Цикл по сообщениям telegram полученных ботом
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
        logger.info(f"chat_id={chat_id}")
        if chat_id > 0:
            # username как оказалось может и не быть - https://gist.github.com/MinistrBob/6bdca92c42d5de2b4204369fb213c892
            username = None
            try:
                username = f"@{update['message']['chat']['username'].lower()}"
            except:
                logger.error(f"username не найден")
            # Ищем в БД участника по telegram username если он есть
            # если username нет то такое сообщение игнорируется
            if username is not None:
                logger.info(f"Поиск по username={username}")
                person = dbconnect.find_participant_by_telegram_username(username)
                logger.info(person)
                if person is None:
                    # Ничего не нашлось. Значит человек добавил себе бота, но пока еще не оплатил,
                    # т.к. запись в таблице появляется только после оплаты,
                    # поэтому заносим его в специальный список, как только оплатит, получит оповещение в Telegram.
                    logger.info(f"Нет участника с таким telegram username={username}")
                    # Добавляем этого пользователя в telegram_bot_added
                    try:
                        sql_text = f"INSERT INTO telegram_bot_added (telegram_id, telegram_username, insert_date) VALUES (%s, %s, NOW())"
                        values_tuple = (chat_id, username)
                        rowcount = dbconnect.execute_dml(sql_text, values_tuple)
                    except:
                        raise_error("Не могу выполнить INSERT INTO telegram_bot_added", logger, prog_name="sf_telegram_bot.py")
                    mark_telegram_update_id(telegram_update_id, logger)
                else:
                    if person['telegram_id'] is None:
                        # Это новый пользователь, ему нужно отправить логин
                        message = get_participant_notification_text(person['last_name'],
                                                                    person['first_name'],
                                                                    person['login'],
                                                                    person['password'])
                        logger.info(f"message=\n{message}")
                        send_message(tb, chat_id, message, logger)
                        # Если да - отметить в БД:
                        # 1) внести telegram_id в participants
                        sql_text = f"UPDATE participants SET telegram_id=%s where id=%s RETURNING id;"
                        values_tuple = (chat_id, person['id'])
                        id_ = dbconnect.execute_dml_id(sql_text, values_tuple)
                        logger.info(f"id_={id_}")
                        if not id_:
                            raise_error(f"Не могу обновить telegram_id={person['telegram_id']} для участника id={person['id']}", logger, prog_name="sf_telegram_bot.py")
                        mark_telegram_update_id(telegram_update_id, logger)
                        logger.info('\n' + '#' * 120)
                    else:
                        logger.info(f"Ничего не отправляю, это старый участник telegram_id={person['telegram_id']}")
                        mark_telegram_update_id(telegram_update_id, logger)
    # Процедура обработки списка проверки telegram_bot_added
    logger.info('Процедура обработки списка проверки telegram_bot_added')
    rows = dbconnect.execute_select(f"select telegram_id, telegram_username from telegram_bot_added where new=FALSE", None)
    if not rows:
        logger.info("Списко проверки пустой")
    else:
        for row in rows:
            logger.info(f"Поиск по username={row[1]}")
            person = dbconnect.find_participant_by_telegram_username(row[1])
            logger.info(person)
            if person:
                message = get_participant_notification_text(person['last_name'],
                                                            person['first_name'],
                                                            person['login'],
                                                            person['password'])
                send_message(tb, person['telegram_id'], message, logger)
        # Сбросить все строки (new) в telegram_bot_added в FALSE
        sql_text = f"UPDATE telegram_bot_added set new=FALSE where new=TRUE"
        rowcount = dbconnect.execute_dml(sql_text, None)
        logger.info(f"rowcount={rowcount}")
    # Удаление строк из telegram_bot_added старше 31 дней.
    sql_text = f"delete from telegram_bot_added where insert_date < NOW() - INTERVAL '31 days'"
    rowcount = dbconnect.execute_dml(sql_text, None)
    logger.info(f"rowcount={rowcount}")

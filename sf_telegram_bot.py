import requests
import PASSWORDS
import sys
from DBPostgres import DBPostgres
from alert_to_mail import send_error_to_admin, get_participant_notification_text


class TelegramBot:
    """
    Простейший класс Telegram бота
    """
    def __init__(self, bot_url, logger_, database=None):
        self.bot_url = bot_url
        self.logger = logger_
        self.database = database

    def get_text_updates(self, offset=0):
        """
        Get updates from Telegram
        :return: Dictionary Updates
        """
        params = {'timeout': 1, 'offset': offset, 'limit': 1000, 'allowed_updates': ['message', 'edited_message']}
        response = requests.get(self.bot_url + '/getUpdates', data=params)
        self.logger.debug(response)
        self.logger.debug(response.json())
        if response.ok:
            self.logger.debug("get_updates_json OK")
            return True, response.json()
        else:
            self.logger.error(f"ERROR:{response.text}")
            return False, response.text

    def send_text_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.bot_url + '/sendMessage', data=params)
        self.logger.debug(response)
        if response.ok:
            self.logger.debug("get_updates_json ОК")
            return True, None
        else:
            self.logger.error(f"ERROR:{response.text}")
            return False, response.text


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


def raise_error(err_text_, logger_):
    """
    Записать в лог ошибку - Выслать ошибку админу - Генерировать исключение
    :param err_text_: Текст ошибки
    :param logger_: логгер
    """
    logger_.error(err_text_)
    send_error_to_admin(err_text_, logger_, prog_name="sf_telegram_bot.py")
    raise Exception(err_text_)


if __name__ == '__main__':
    import custom_logger
    import os

    logger = custom_logger.get_logger(program_file=os.path.realpath(__file__))
    logger.info("Try connect to DB")
    try:
        dbconnect = DBPostgres(dbname=PASSWORDS.logins['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                               password=PASSWORDS.logins['postgres_password'],
                               host=PASSWORDS.logins['postgres_host'],
                               port=PASSWORDS.logins['postgres_port'], logger=logger)
    except Exception:
        raise_error("Can't connect to DB!!!", logger)
        sys.exit(1)
    # logger.info('\n' + '#' * 120)
    # Получить update_id из БД
    rows = dbconnect.execute_select(f"select value from settings where key='telegram_update_id';", None)
    logger.debug(f"rows={rows}")
    if not rows:
        raise_error("Select для telegram_update_id ничего не возвращает", logger)
    try:
        telegram_update_id = int(rows[0][0])
    except:
        raise_error("Не могу получить telegram_update_id из БД", logger)
    logger.debug(f"telegram_update_id={telegram_update_id}")
    tb = TelegramBot(PASSWORDS.logins['telegram_bot_url'], logger)
    logger.info("Get updates")
    success, updates = tb.get_text_updates(telegram_update_id)
    logger.debug(f"success={success}")
    logger.debug(f"updates=\n{updates}")
    if not success:
        raise_error(f"Не могу получить updates\n{updates}", logger)
    for update in updates['result']:
        try:
            telegram_update_id = int(update['update_id'])
        except:
            raise_error("Не могу получить telegram_update_id из update", logger)
        logger.info(f"Processing telegram_update_id={telegram_update_id}")
        try:
            chat_id = update['message']['chat']['id']
        except:
            raise_error("Не могу получить chat_id", logger)
        logger.debug(f"chat_id={chat_id}")
        if chat_id > 0:
            try:
                username = f"@{update['message']['chat']['username'].lower()}"
            except:
                raise_error("Не могу получить username", logger)
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
                        raise_error(f"Не могу отправить сообщение\n{result}", logger)
                    # Если да - отметить в БД:
                    # 1) внести telegram_id в participants
                    sql_text = f"UPDATE participants SET telegram_id=%s where id=%s RETURNING id;"
                    values_tuple = (chat_id, person['id'])
                    id_ = dbconnect.execute_dml_id(sql_text, values_tuple)
                    logger.debug(f"id_={id_}")
                    if not id_:
                        raise_error(f"Не могу обновить telegram_id={person['telegram_id']} для участника id={person['id']}", logger)
                    mark_telegram_update_id(telegram_update_id, logger)
                    logger.info('\n' + '#' * 120)
                else:
                    logger.info(f"Ничего не отправляю, это старый участник telegram_id={person['telegram_id']}")
                    mark_telegram_update_id(telegram_update_id, logger)

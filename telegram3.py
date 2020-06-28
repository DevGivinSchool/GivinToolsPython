import requests
import PASSWORDS
import traceback
import sys
from DBPostgres import DBPostgres
from alert_to_mail import send_mail
from alert_text import get_participant_notification_text


# import logging


def get_chat_id(data):
    """
    Method to extract chat id from telegram request.
    """
    chat_id = data['message']['chat']['id']
    print(chat_id)
    return chat_id


def get_chat_username(data):
    """
    Method to extract username from telegram request.
    """
    chat_username = data['message']['chat']['username']
    print(chat_username)
    return chat_username


def get_message(data):
    """
    Method to extract message id from telegram request.
    """
    message_text = data['message']['text']
    print(message_text)
    return message_text


class TelegramBot:
    def __init__(self, bot_url, logger, database=None):
        self.bot_url = bot_url
        self.logger = logger
        self.database = database

    def get_updates_json(self, offset=0):
        """
        Get updates from Telegram
        :return: Dictionary Updates
        """
        params = {'timeout': 100, 'offset': offset, 'limit': 1000, 'allowed_updates': ['message', 'edited_message']}
        response = requests.get(self.bot_url + '/getUpdates', data=params)
        self.logger.debug(response)
        self.logger.debug(response.json())
        if response.ok:
            self.logger.debug("get_updates_json ОК")
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


if __name__ == '__main__':
    import logging
    from Log import Log
    from log_config import log_dir

    log_level = logging.DEBUG
    logger = Log.setup_logger('__main__', log_dir, log_name=f'telegram_bot', level=log_level, dt="%Y%m%d%H%M")

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
    logger.info('\n' + '#' * 120)

    tb = TelegramBot(PASSWORDS.logins['telegram_bot_url'], logger)
    success, updates = tb.get_updates_json()
    if not success:
        raise Exception(f"Не могу получить updates\n{updates}")
    print(updates)
    exit(0)
    # lu = last_update(updates)
    for lu in updates['result']:
        chat_id = get_chat_id(lu)
        logger.debug(f"chat_id={chat_id}")
        if chat_id > 0:
            username = get_chat_username(lu)
            logger.debug(f"username={username}")
            person = dbconnect.find_participant_by_telegram_username(username)
            logger.debug(person)
            if person is None:
                # Ничего не нашлось
                logger.debug(f"Нет участника с таким telegram username {username}")
            else:
                if person['telegram_id'] is None:
                    # Это новый пользователь, ему нужно отправить логин
                    message = get_participant_notification_text(person['last_name'],
                                                                person['first_name'],
                                                                person['login'],
                                                                person['password'])
                    success, result = tb.send_text_message(chat_id, message)
                    if not success:
                        raise Exception(f"Не могу отправить сообщение\n{result}")
                    # если да - отметить в БД 1) внести telegram_id 2) зафиксировать update_id
                    sql_text = f"UPDATE participants SET telegram_id=%s where id=%s RETURNING id;"
                    values_tuple = (person['telegram_id'], person['id'])
                    id_ = dbconnect.execute_dml_id(sql_text, values_tuple)
                    if not id_:
                        raise Exception(
                            f"Не могу обновить telegram_id={person['telegram_id']} для участника id={person['id']}")

                    # TODO: нужно получить update_id из БД в начале процедуры
                    sql_text = f"UPDATE settings SET key=%s where key='telegram_id' RETURNING key;"
                    values_tuple = (person['telegram_id'], person['id'])
                    id_ = dbconnect.execute_dml_id(sql_text, values_tuple)
                    # TODO: переписать процедуру получения updates с последнего update_id

# TODO: В каждом alert сделать отсылку письма админу.
# TODO: Везде вставить log.debug

"""
<Response [200]>
{'ok': True, 'result': [{'update_id': 391387715, 'message': {'message_id': 20, 'from': {'id': 324846110, 'is_bot': False, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'language_code': 'ru'}, 'chat': {'id': 324846110, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'type': 'private'}, 'date': 1593108194, 'text': 'Test for link www.mail.ru  dsfhdsjfadsjf 3254', 'entities': [{'offset': 14, 'length': 11, 'type': 'url'}]}}]}
[{'update_id': 391387715, 'message': {'message_id': 20, 'from': {'id': 324846110, 'is_bot': False, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'language_code': 'ru'}, 'chat': {'id': 324846110, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'type': 'private'}, 'date': 1593108194, 'text': 'Test for link www.mail.ru  dsfhdsjfadsjf 3254', 'entities': [{'offset': 14, 'length': 11, 'type': 'url'}]}}]
0
{'update_id': 391387715, 'message': {'message_id': 20, 'from': {'id': 324846110, 'is_bot': False, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'language_code': 'ru'}, 'chat': {'id': 324846110, 'first_name': 'Дмитрий', 'last_name': 'Бобровский', 'username': 'BobrD', 'type': 'private'}, 'date': 1593108194, 'text': 'Test for link www.mail.ru  dsfhdsjfadsjf 3254', 'entities': [{'offset': 14, 'length': 11, 'type': 'url'}]}}
324846110
<Response [200]>
"""

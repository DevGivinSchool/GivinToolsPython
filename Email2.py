import email
import re
import config
import Parser
import PASSWORDS
import traceback
from Log import Log
from Task import Task
from email.header import decode_header
from DBPostgres import DBPostgres

# def string_normalization(msg):
#    return msg.strip().lstrip("<").rstrip(">")


def get_from(line):
    """Выбираем только первый почтовый адрес из строки"""
    match = re.findall(r'[\w\.-]+@[\w\.-]+', line)
    return match[0]


def get_decoded_str(line):
    """Decode email field - From.
    :param line: Raw 7-bit message body input e.g. from imaplib.
    :return: Body of the letter in the desired encoding
    """
    lines = decode_header(line)
    final_text = ""
    for text, charset in lines:
        # print(text, charset)
        if charset is None:
            # Здесь нет final_text = final_text + ... поэтому в итоге будет только самая последняя строка много
            # страничного From. Обычно это правильно, т.к. в начале часто ставиться фамилия а затем email.
            try:
                final_text = text.decode()
            except AttributeError:
                final_text = text
        else:
            final_text = text.decode(str(charset), "ignore")
    return final_text


class Email:
    """Kласс для работы с почтой"""

    def __init__(self, client, logger):
        self.client = client
        self.logger = logger  # Общий logger для всей программы
        self.work_logger = logger  # Частный логгер для каждого письма а затем и Task

    def sort_mail(self):
        """Sort mail and start work """
        self.logger.info("sort_mail beggin")
        try:
            postgres = DBPostgres(dbname=config.config['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                              password=PASSWORDS.logins['postgres_password'], host=config.config['postgres_host'],
                              port=config.config['postgres_port'])
        except Exception as err:
            print("MAIN ERROR (Postgres):\n" + traceback.format_exc())

        # TODO: Здесь нужно сделать провеку есть ли незавершенные сесии и если есть отправить письмо админу,
        #       а в такой сессии после отправки письма проставить признак что отправлено оповещение
        #       дату отправки проставлять в поле завершения, а признак в поле признака
        sessin_id = postgres.session_begin()
        messages = self.client.search('ALL')
        """We go through the cycle in all letters"""
        for uid, message_data in self.client.fetch(messages, 'RFC822').items():
            """Get main parameters letters"""
            uuid = str(uid)
            self.work_logger = Log.setup_logger(uuid, config.config['log_dir'], f'{uuid}.log',
                                                config.config['log_level'])
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            self.work_logger.info("RAW EMAIL MESSAGE")
            self.work_logger.debug(f"email_message.get_content_charset()={email_message.get_content_charset()}")
            self.work_logger.debug(f"email_message.get_charset()={email_message.get_charset()}")
            self.work_logger.info("=" * 45)
            self.work_logger.info(email_message)
            self.work_logger.info("=" * 45)
            self.work_logger.info(f"uid={uuid}")
            self.work_logger.debug(f"raw_ffrom=|{email_message.get('From')}|")
            self.work_logger.debug(f"raw_fsubject=|{email_message.get('Subject')}|")
            ffrom = get_from(get_decoded_str(email_message.get('From')))
            # fsubject = email_message.get('Subject')
            fsubject = get_decoded_str(email_message.get('Subject'))
            self.work_logger.info(f"ffrom={ffrom}")
            self.work_logger.info(f"fsubject={fsubject}")
            body = self.get_decoded_email_body(email_message)
            # Create Task and insert it to DB
            task = Task(uuid, ffrom, fsubject, body, self.work_logger)
            postgres.create_task(sessin_id, task)

            """Определяем типа письма (платёж / не платёж) и вытаскиваем данные платежа в payment."""
            payment = {}
            # TODO: Нужно результаты обработки писем заносить в БД и потом в Email2 получить сводку и отправлять админу.
            # В PayKeeper могут быть платежи не за ДШ а за что-то другое
            if ffrom == 'noreply@server.paykeeper.ru' and fsubject == 'Принята оплата':
                self.logger.debug(f'Это письмо от платежной системы - PayKeeper')
                # print(f'Это письмо от платежной системы - PayKeeper')
                payment = Parser.parse_paykeeper_html(body['body_html'])
                self.logger.debug(f'payment = {payment}')
                # Put in Payment to Task and insert Payment to DB
                task.payment = payment
                postgres.create_payment(task)
                # Это платёж PayKeeper за ДШ
                if self.check_school_friends(payment["Наименование услуги"]):
                    print('Это платёж Друзья Школы')
                    self.logger.debug('Это платёж Друзья Школы')
                    # TODO: Процедура обработки payment
                # Это платёж PayKeeper но НЕ за ДШ
                else:
                    print('Это ИНОЙ платёж')
                    self.logger.debug('Это ИНОЙ платёж')
                    # TODO: Нужно результаты обработки писем заносить в БД и потом в Email2 получить сводку и отправлять админу.
            # В Getcourse только платежи за ДШ иного там нет
            elif ffrom == 'no-reply@getcourse.ru' and fsubject.startswith("Поступил платеж"):
                self.logger.debug(f'Это письмо от платежной системы - GetCourse')
                # print(f'Это письмо от платежной системы - GetCourse')
                payment = Parser.parse_getcourse_html(body['body_html'])
                self.logger.debug(f'payment = {payment}')
                # Put in Payment to Task and insert Payment to DB
                task.payment = payment
                postgres.create_payment(task)
                # TODO: Процедура обработки payment
            # Это письмо вообще не платёж
            else:
                self.logger.debug(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
                print(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
                # TODO: Нужно результаты обработки писем заносить в БД и потом в Email2 получить сводку и отправлять админу.
            print('-' * 45)

            if payment:
                self.logger.info(f"payment for {ffrom}:\n{payment}")
            # TODO: -----------------------------------------------------------------
        postgres.session_end()
        self.logger.info("sort_mail end")

    def get_decoded_email_body(self, msg):
        """Decode email body.
        Detect character set if the header is not set. We try to get text/plain.
        :param msg: Raw 7-bit message body input e.g. from imaplib.
        :return: Body of the letter in the desired encoding
        """
        body = {'body_type': '', 'body_text': '', 'body_html': ''}
        text = ""
        html = ""
        if msg.is_multipart():
            self.work_logger.debug("multipart body")
            for part in msg.get_payload():

                charset = part.get_content_charset()
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition')).replace("\r", ' ').replace("\n", ' ')
                self.work_logger.debug(f"{content_type}|{charset}|{content_disposition}")

                if content_type == 'text/html':
                    html = html + part.get_payload(decode=True).decode(str(charset), "ignore")
                # This is text and not attachment
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    # text = part.get_payload(decode=True).decode(str(charset), "ignore").encode('utf8', 'replace')
                    text = text + part.get_payload(decode=True).decode(str(charset), "ignore")
        else:
            self.work_logger.debug("singlepart body")
            charset = msg.get_content_charset()
            content_type = msg.get_content_type()
            self.work_logger.debug(f"{content_type}|{charset}")
            # text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
            if content_type == 'text/html':
                html = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
            if content_type == 'text/plain':
                text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
        body['body_text'] = text
        body['body_html'] = html
        if len(text) > 0 and len(html) > 0:
            body['body_type'] = 'mix'
            self.work_logger.debug(f"body_type={body['body_type']}")
            self.work_logger.debug(f"body_text={body['body_text']}")
            self.work_logger.debug(f"body_html={body['body_html']}")
        elif len(text) > 0 and len(html) == 0:
            body['body_type'] = 'text'
            self.work_logger.debug(f"body_type={body['body_type']}")
            self.work_logger.debug(f"body_text={body['body_text']}")
        elif len(text) == 0 and len(html) > 0:
            body['body_type'] = 'html'
            self.work_logger.debug(f"body_type={body['body_type']}")
            self.work_logger.debug(f"body_html={body['body_html']}")
        else:
            raise Exception('Неизвестный формат письма')

        return body

    def check_school_friends(self, text):
        """Проверяем что назначение платежа - Друзья школы"""
        text_lower = text.lower()
        list_ofstrs = ['друзья', 'школы']
        # Check if all strings from the list exists in given string
        result = all(([True if sub_str in text_lower else False for sub_str in list_ofstrs]))
        return result

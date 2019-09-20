import email
import re
import config
import Parser
import PASSWORDS
import traceback
import sys
from Log import Log
from Task import Task
from email.header import decode_header
from DBPostgres import DBPostgres
from alert_to_mail import send_mail


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
        # self.work_logger = logger  # Частный логгер для каждого письма а затем и Task

    def sort_mail(self):
        """Sort mail and start work """
        self.logger.info("sort_mail beggin")
        try:
            postgres = DBPostgres(dbname=config.config['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                                  password=PASSWORDS.logins['postgres_password'], host=config.config['postgres_host'],
                                  port=config.config['postgres_port'])
        except Exception as err:
            error_text = "MAIN ERROR (Postgres):\n" + traceback.format_exc()
            print(error_text)
            send_mail(PASSWORDS.logins['admin_emails'], error_text)
            sys.exit(1)

        # TODO: Здесь нужно сделать провеку есть ли незавершенные сесии и если есть отправить письмо админу,
        #       а в такой сессии после отправки письма проставить признак что отправлено оповещение
        #       дату отправки проставлять в поле завершения, а признак в поле признака
        sessin_id = postgres.session_begin()
        self.logger.info(f'Start session = {sessin_id}')
        messages = self.client.search('ALL')
        """We go through the cycle in all letters"""
        for uid, message_data in self.client.fetch(messages, 'RFC822').items():
            """Get main parameters letters"""
            uuid = str(uid)
            # self.work_logger = Log.setup_logger(uuid, config.config['log_dir'], f'{uuid}.log',
            #                                     config.config['log_level'])
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            self.logger.debug("RAW EMAIL MESSAGE")
            self.logger.debug(f"email_message.get_content_charset()={email_message.get_content_charset()}")
            self.logger.debug(f"email_message.get_charset()={email_message.get_charset()}")
            self.logger.debug("=" * 45)
            self.logger.debug(email_message)
            self.logger.debug("=" * 45)
            self.logger.debug(f"uid={uuid}")
            self.logger.debug(f"raw_ffrom=|{email_message.get('From')}|")
            self.logger.debug(f"raw_fsubject=|{email_message.get('Subject')}|")
            ffrom = get_from(get_decoded_str(email_message.get('From')))
            # fsubject = email_message.get('Subject')
            fsubject = get_decoded_str(email_message.get('Subject'))
            self.logger.debug(f"ffrom={ffrom}")
            self.logger.debug(f"fsubject={fsubject}")
            body = self.get_decoded_email_body(email_message)
            # Create Task and insert it to DB
            task = Task(uuid, ffrom, fsubject, body, self.logger)
            task_is_new = postgres.create_task(sessin_id, task)
            self.logger.info(f"Task {sessin_id}:{uuid}:{task_is_new} begin")
            if task_is_new:
                try:
                    """Определяем типа письма (платёж / не платёж) и вытаскиваем данные платежа в payment."""
                    # В PayKeeper могут быть платежи не за ДШ а за что-то другое
                    if ffrom == 'noreply@server.paykeeper.ru' and fsubject == 'Принята оплата':
                        self.logger.info(f'Это письмо от платежной системы - PayKeeper')
                        # print(f'Это письмо от платежной системы - PayKeeper')
                        payment = Parser.parse_paykeeper_html(body['body_html'])
                        # Пока создание платежа перенесу отсюда - ниже в, чтобы в БД создавались платежи только ДШ
                        # self.create_payment(payment, postgres, task)
                        # Это платёж PayKeeper за ДШ
                        if self.check_school_friends(payment["Наименование услуги"]):
                            # print('Это платёж Друзья Школы')
                            self.logger.info('Это платёж Друзья Школы')
                            self.create_payment(payment, postgres, task)
                            task.task_run()
                        # Это платёж PayKeeper но НЕ за ДШ
                        else:
                            # print('Это ИНОЙ платёж')
                            self.logger.info('Это ИНОЙ платёж')
                    # В Getcourse только платежи за ДШ иного там нет
                    elif ffrom == 'no-reply@getcourse.ru' and fsubject.startswith("Поступил платеж"):
                        self.logger.info(f'Это письмо от платежной системы - GetCourse')
                        # print(f'Это письмо от платежной системы - GetCourse')
                        payment = Parser.parse_getcourse_html(body['body_html'])
                        self.create_payment(payment, postgres, task)
                        task.task_run()
                    # Это письмо вообще не платёж
                    else:
                        self.logger.info(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
                        # print(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
                    # if payment:
                    #    self.logger.info(f"payment for {ffrom}:\n{payment}")
                except Exception as e:
                    error_text = "PAYMENT ERROR:\n" + traceback.format_exc()
                    # print(error_text)
                    postgres.task_error()
                    self.logger.error(error_text)
                    self.logger.info('-' * 45)
                    continue
            else:
                self.logger.info(f"Это письмо уже обрабатывалось")
            self.logger.info(f"Task {sessin_id}:{uuid}:{task_is_new} end")
            # print('-' * 45)
            self.logger.info('-' * 45)
            # -----------------------------------------------------------------
        postgres.session_end(sessin_id)
        self.logger.info(f'End session = {sessin_id}')
        # TODO: Нужно результаты обработки писем заносить в БД и потом в Email2 получить сводку и отправлять админу.
        self.logger.info("sort_mail end")

    def create_payment(self, payment, postgres, task):
        self.logger.info("create_payment begin")
        self.logger.info(f'payment = {payment}')
        # Put in Payment to Task and insert Payment to DB
        task.payment = payment
        payment_id, participant_id = postgres.create_payment(task)
        task.payment["payment_id"] = payment_id
        task.payment["participant_id"] = participant_id
        self.logger.info(f"Payment {payment_id} for participant {participant_id} created")
        self.logger.info("create_payment end")

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
            self.logger.debug("multipart body")
            for part in msg.get_payload():

                charset = part.get_content_charset()
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition')).replace("\r", ' ').replace("\n", ' ')
                self.logger.debug(f"{content_type}|{charset}|{content_disposition}")

                if content_type == 'text/html':
                    html = html + part.get_payload(decode=True).decode(str(charset), "ignore")
                # This is text and not attachment
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    # text = part.get_payload(decode=True).decode(str(charset), "ignore").encode('utf8', 'replace')
                    text = text + part.get_payload(decode=True).decode(str(charset), "ignore")
        else:
            self.logger.debug("singlepart body")
            charset = msg.get_content_charset()
            content_type = msg.get_content_type()
            self.logger.debug(f"{content_type}|{charset}")
            # text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
            if content_type == 'text/html':
                html = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
            if content_type == 'text/plain':
                text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
        body['body_text'] = text
        body['body_html'] = html
        if len(text) > 0 and len(html) > 0:
            body['body_type'] = 'mix'
            self.logger.debug(f"body_type={body['body_type']}")
            self.logger.debug(f"body_text={body['body_text']}")
            self.logger.debug(f"body_html={body['body_html']}")
        elif len(text) > 0 and len(html) == 0:
            body['body_type'] = 'text'
            self.logger.debug(f"body_type={body['body_type']}")
            self.logger.debug(f"body_text={body['body_text']}")
        elif len(text) == 0 and len(html) > 0:
            body['body_type'] = 'html'
            self.logger.debug(f"body_type={body['body_type']}")
            self.logger.debug(f"body_html={body['body_html']}")
        else:
            raise Exception('Неизвестный формат письма')

        return body

    def check_school_friends(self, text):
        """Проверяем что назначение платежа - Друзья школы"""
        text_lower = text.lower()
        # print(f'text_lower={text_lower}')
        list_ofstrs = ['дш', 'друзья', 'школы']
        # print(f'list_ofstrs={list_ofstrs}')
        # Check if all strings from the list exists in given string
        result = False
        for sub_str in list_ofstrs:
            if sub_str in text_lower:
                result = True
                break
        # result = all(([True if sub_str in text_lower else False for sub_str in list_ofstrs]))
        # print(f'result={result}')
        return result

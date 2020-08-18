import email
import re
import sys
import traceback
from email.header import decode_header
import html2text
import PASSWORDS
import payment_creater
from Class_DBPostgres import DBPostgres
from Class_Task import Task
from alert_to_mail import raise_error


def get_first_email_from_line(line):
    """Выбираем только первый почтовый адрес из строки"""
    match = re.findall(r'[\w\.-]+@[\w\.-]+', line)
    if len(match) > 0:
        return match[0]
    else:
        return None


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


def verification_for_school_friends(text):
    """Проверяем что назначение платежа - Друзья школы"""
    text_lower = text.lower().strip()
    # print(f'text_lower={text_lower}')
    list_ofstrs = ['дш', 'друзья школы', 'д.ш.', 'друзей школы']
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


class Email:
    """Kласс для работы с почтой"""

    def __init__(self, client, postgres, session_id, logger):
        self.client = client
        self.logger = logger  # Общий logger для всей программы
        # self.work_logger = logger  # Частный логгер для каждого письма а затем и Task
        self.postgres = postgres  # Соединение с БД
        self.session_id = session_id

    def move_email_to_trash(self, uuid):
        self.logger.info(f"Удаляю сообщение: {uuid}")
        self.client.move(uuid, "Archive")

    def sort_mail(self):
        """Sort mail and start work """
        self.logger.info("sort_mail begin")
        messages = self.client.search('ALL')
        """We go through the cycle in all letters"""
        for uid, message_data in self.client.fetch(messages, 'RFC822').items():
            """Get main parameters letters"""
            uuid = str(uid)
            print(uuid)
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
            ffrom = get_first_email_from_line(get_decoded_str(email_message.get('From')))
            # fsubject = email_message.get('Subject')
            fsubject = get_decoded_str(email_message.get('Subject'))
            self.logger.debug(f"ffrom={ffrom}")
            self.logger.debug(f"fsubject={fsubject}")
            body = self.get_decoded_email_body(email_message)
            if body is None:
                error_text = 'ERROR: Неизвестный формат письма'
                self.logger.error(error_text)
                if uuid is not None:
                    self.logger.error(f"UUID: {uuid}")
                if ffrom is not None:
                    self.logger.error(f"FROM: {ffrom}")
                if fsubject is not None:
                    self.logger.error(f"SUBJECT: {fsubject}")
                if body is not None:
                    if body['body_type'] == 'mix':
                        self.logger.error(f"BODY\n: {body['body_text']}")
                    elif body['body_type'] == 'html':

                        self.logger.error(f"BODY\n: {body['body_html']}")
                    else:
                        self.logger.error(f"BODY\n: {body['body_text']}")
                self.logger.info('-' * 45)
                self.postgres.task_error(error_text, uuid)
                raise_error(f"TASK {uuid} ERROR: {error_text}", self.logger, prog_name="Class_Email.py")
                self.move_email_to_trash(uuid)
                continue
            # Create Task and insert it to DB
            task = Task(uuid, ffrom, fsubject, self.logger, self.postgres)
            task_is_new = self.postgres.create_task(self.session_id, task)
            self.logger.info(f"Task begin: ID={uuid}|NEW={task_is_new}")
            if task_is_new:
                try:
                    """Определяем типа письма (платёж / не платёж) и вытаскиваем данные платежа в payment."""
                    # PayKeeper
                    if ffrom == 'noreply@server.paykeeper.ru' and fsubject == 'Принята оплата':
                        self.logger.info(f'Это письмо от платежной системы - PayKeeper')
                        try:
                            payment = payment_creater.parse_paykeeper_html(body['body_html'], self.logger)
                        except Exception:
                            raise_error("ERROR: parse_paykeeper_html", self.logger, prog_name="Class_Email.py")
                            sys.exit(1)
                        self.payment_verification_for_school_friends(ffrom, fsubject, payment, self.postgres, task, uuid)
                    # Getcourse
                    elif (
                            ffrom == 'no-reply@getcourse.ru' or ffrom == 'info@study.givinschool.org' or ffrom == 'info@givin.school') \
                            and fsubject.startswith("Поступил платеж"):
                        self.logger.info(f'Это письмо от платежной системы - GetCourse')
                        # print(f'Это письмо от платежной системы - GetCourse')
                        try:
                            payment = payment_creater.parse_getcourse_html(body['body_html'], self.logger)
                        except Exception:
                            raise_error("ERROR: parse_getcourse_html", self.logger, prog_name="Class_Email.py")
                            sys.exit(1)
                        self.payment_verification_for_school_friends(ffrom, fsubject, payment, self.postgres, task, uuid)
                    # Это письмо вообще не платёж
                    else:
                        self.logger.info(f'ЭТО ПИСЬМО НЕ ОТ ПЛАТЁЖНЫХ СИСТЕМ (ничего с ним не делаю, пока...)')
                        # print(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
                        # Если в тема письма начинается на #
                        # значит это команда иначе удалить
                        if not fsubject.startswith("#"):
                            if uuid is not None:
                                self.logger.info(f"    UUID   : {uuid}")
                            if ffrom is not None:
                                self.logger.info(f"    FROM   : {ffrom}")
                            if fsubject is not None:
                                self.logger.info(f"    SUBJECT: {fsubject}")
                            if body is not None:
                                self.logger.info(f"    body_type: {body['body_type']}")
                                if body['body_type'] == 'mix':
                                    self.logger.info(f"    BODY\n: {body['body_text']}")
                                elif body['body_type'] == 'html':
                                    # Преобразование письма в формате html в текст
                                    self.logger.info(f"Преобразование письма в формате html в текст")
                                    h = html2text.HTML2Text()
                                    h.ignore_links = False
                                    h.single_line_break = True
                                    body_html = h.handle(body['body_html'])
                                    self.logger.info(f"    BODY\n: {body_html}")
                                else:
                                    self.logger.info(f"    BODY\n: {body['body_text']}")
                            self.move_email_to_trash(uuid)
                        else:
                            # Процедура обработки писем с командами (fsubject.startswith("#"))
                            # https://github.com/DevGivinSchool/GivinToolsPython/projects/1#card-41171908
                            pass
                    # if payment:
                    #    self.logger.info(f"payment for {ffrom}:\n{payment}")
                except Exception:
                    error_text = "TASK ERROR:\n" + traceback.format_exc()
                    # print(uuid, error_text)

                    self.logger.error(error_text)
                    if uuid is not None:
                        self.logger.error(f"UUID: {uuid}")
                    if ffrom is not None:
                        self.logger.error(f"FROM: {ffrom}")
                    if fsubject is not None:
                        self.logger.error(f"SUBJECT: {fsubject}")
                    if body is not None:
                        if body['body_type'] == 'mix':
                            self.logger.error(f"BODY\n: {body['body_text']}")
                        elif body['body_type'] == 'html':

                            self.logger.error(f"BODY\n: {body['body_html']}")
                        else:
                            self.logger.error(f"BODY\n: {body['body_text']}")
                    self.logger.info('-' * 45)
                    self.postgres.task_error(error_text, uuid)
                    raise_error(f"TASK {uuid} ERROR: {error_text}", self.logger, prog_name="Class_Email.py")
                    continue
            else:
                self.logger.warning(f"ВНИМАНИЕ: Это письмо уже обрабатывалось!")
            self.logger.info(f"Task end: ID={uuid}|NEW={task_is_new}")
            print(uuid)
            # print('-' * 45)
            self.logger.info('=' * 45)
            self.logger.info('=' * 45)
            self.logger.info('=' * 45)
            # -----------------------------------------------------------------
        self.client.expunge()
        self.logger.info("sort_mail end")

    def payment_verification_for_school_friends(self, ffrom, fsubject, payment, postgres, task, uuid):
        """
        Проверка платежа что он для Друзей Школы.
        Если да, тогда обрабатываем этот платёж.
        Если нет, выводим информацию в лог.
        В любом случае письмо перемещается в Корзину.
        :param ffrom: От кого письмо
        :param fsubject: Тема письма
        :param payment: Платёж
        :param postgres: Соединение с БД
        :param task: Задача по обработке письма
        :param uuid: UUID письма
        :return:
        """
        if verification_for_school_friends(payment["Наименование услуги"]):
            # print('Это платёж Друзья Школы')
            self.logger.info('Это платёж Друзья Школы')
            self.create_payment(payment, postgres, task)
            task.task_run()
        # Это платёж но НЕ за ДШ
        else:
            self.logger.info('ЭТО ИНОЙ ПЛАТЁЖ')
            if uuid is not None:
                self.logger.info(f"    UUID   : {uuid}")
            if ffrom is not None:
                self.logger.info(f"    FROM   : {ffrom}")
            if fsubject is not None:
                self.logger.info(f"    SUBJECT: {fsubject}")
            if fsubject is not None:
                self.logger.info(f'    PAYMENT: {payment}')
            """
            if body is not None:
                self.logger.info(f"body_type: {body['body_type']}")
                if body['body_type'] == 'mix':
                    self.logger.info(f"BODY\n: {body['body_text']}")
                elif body['body_type'] == 'html':
                    self.logger.info(f"BODY\n: {body['body_html']}")
                else:
                    self.logger.info(f"BODY\n: {body['body_text']}")
            """
        self.move_email_to_trash(uuid)

    def create_payment(self, payment, postgres, task):
        self.logger.info(">>>>Class_Email.create_payment begin")
        # This payment after parsing mail
        self.logger.info(f'payment after parsing = {payment}')
        # Put in Payment to Task and insert Payment to DB
        # and join payment after parsing with participant if it is
        task.payment = payment
        payment_id, participant_id, participant_type = postgres.create_payment(task)
        task.payment["task_uuid"] = payment_id
        task.payment["participant_id"] = participant_id
        task.payment["participant_type"] = participant_type
        self.logger.info(f"Payment {payment_id} for participant {participant_id}|{participant_type} created")
        self.logger.info(">>>>Class_Email.create_payment end")

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
            # raise Exception('Неизвестный формат письма')
            return None
        return body

import email
import re
from email.header import decode_header

import config
from Log import Log
from Task import Task


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
        """Sort mail and start work.
        """
        self.logger.info("sort_mail")
        messages = self.client.search('ALL')
        for uid, message_data in self.client.fetch(messages, 'RFC822').items():
            uuid = str(uid)
            self.work_logger = Log.setup_logger(uuid, config.config['log_dir'], f'{uuid}.log',
                                                config.config['log_level'])
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            self.work_logger.info("RAW EMAIL MASSAGE")
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
            task = Task(uuid, ffrom, fsubject, body, self.work_logger)
            # self.executor.add_task(task)
            # TODO: -----------------------------------------------------------------
            # TODO: Нужно вместо task.run_task() перенести определение правильности писем и платежей сбда и сразу формировать списки
            #       paykeeper, paykeeper+это не тот платёж, getcourse и результаты обработки платежа вносить в {}
            payment = task.run_task()
            if payment:
                self.logger.info(f"payment for {ffrom}:\n{payment}")
            # TODO: -----------------------------------------------------------------

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

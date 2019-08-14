import email
from email.header import decode_header
from Task import Task
from Log import Log
import logging
import config


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
            self.work_logger.debug("RAW EMAIL MASSAGE")
            self.work_logger.debug(f"email_message.get_content_charset()={email_message.get_content_charset()}")
            self.work_logger.debug(f"email_message.get_charset()={email_message.get_charset()}")
            self.work_logger.debug("=" * 45)
            self.work_logger.debug(email_message)
            self.work_logger.debug("=" * 45)
            self.work_logger.debug(f"uid={uuid}")
            self.work_logger.debug(f"raw_ffrom=|{email_message.get('From')}|")
            self.work_logger.debug(f"raw_fsubject=|{email_message.get('Subject')}|")
            ffrom = self.string_normalization(self.get_decoded_str(email_message.get('From')))
            # fsubject = email_message.get('Subject')
            fsubject = self.get_decoded_str(email_message.get('Subject'))
            self.work_logger.debug(f"ffrom={ffrom}")
            self.work_logger.debug(f"fsubject={fsubject}")
            body = self.get_decoded_email_body(email_message)
            self.work_logger.debug(f"body={body}")
            task = Task(uuid, ffrom, fsubject, body, self.work_logger)
            task.display_task()
            # self.executor.add_task(task)

    def string_normalization(self, msg):
        return msg.strip().lstrip("<").rstrip(">")

    def get_decoded_str(self, line):
        """Decode email field - From.
        :param line: Raw 7-bit message body input e.g. from imaplib.
        :return: Body of the letter in the desired encoding
        """
        lines = decode_header(line)
        final_text = ""
        for text, charset in lines:
            # print(text, charset)
            if charset is None:
                # Здесь нет final_text = final_text + ...
                # поэтому в итоге будет только самая последняя строка много страничного From.
                # Обычно это правильно, т.к. в начале часто ставиться фамили а затем email.
                try:
                    final_text = text.decode()
                except AttributeError:
                    final_text = text
            else:
                final_text = text.decode(str(charset), "ignore")
        return final_text

    def get_decoded_email_body(self, msg):
        """Decode email body.
        Detect character set if the header is not set. We try to get text/plain.
        :param msg: Raw 7-bit message body input e.g. from imaplib.
        :return: Body of the letter in the desired encoding
        """

        text = ""
        if msg.is_multipart():
            for part in msg.get_payload():

                self.work_logger.debug(f"{part.get_content_type()}|{part.get_content_charset()}")

                charset = part.get_content_charset()
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))

                # This is text and not attachment
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    # text = part.get_payload(decode=True).decode(str(charset), "ignore").encode('utf8', 'replace')
                    text = text + part.get_payload(decode=True).decode(str(charset), "ignore")

            return text.strip()
        else:
            # text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
            text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
            return text.strip()

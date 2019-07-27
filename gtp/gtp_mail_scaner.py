from imapclient import IMAPClient
import sys
import os
import logging
import email
from email import policy

log_dir = r"c:\!SAVE\log"
# log_dir = "d:\!SAVE\log"
# log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
log_formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(process)d:%(thread)d - %(message)s')
log_level = logging.DEBUG


# Конфигурация логирования
# logging.basicConfig(
#     format='%(asctime)s - %(levelname)s: %(message)s',
#     level=logging.DEBUG,
#     filename='d:\!SAVE\log\myapp.log',
#     filemode='w'
# )
def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(log_formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


logger = setup_logger('mail_scaner', os.path.join(log_dir, 'mail_scaner.log'), level=log_level)
logger.info('START APP')

if 'ymail_login' in os.environ:
    ymail_login = os.environ.get('ymail_login')
else:
    print("Variable ymail_login is not defined in environment variables")
    logger.error("Variable ymail_login is not defined in environment variables")
    sys.exit(1)
if 'ymail_password' in os.environ:
    ymail_password = os.environ.get('ymail_password')
else:
    print("Variable ymail_password is not defined in environment variables")
    logger.error("Variable ymail_password is not defined in environment variables")
    sys.exit(1)


def get_decoded_email_body(msg):
    """ Decode email body.
    Detect character set if the header is not set.
    We try to get text/plain, but if there is not one then fallback to text/html.
    :param message_body: Raw 7-bit message body input e.g. from imaplib. Double encoded in quoted-printable and latin-1
    :return: Message body as unicode string
    """

    # msg = email.message_from_string(message_body)
    # msg = message_body

    text = ""
    if msg.is_multipart():
        for part in msg.get_payload():

            logger.debug(f"{part.get_content_type()}|{part.get_content_charset()}")

            charset = part.get_content_charset()
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))

            # This is text and not attachment
            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                # text = part.get_payload(decode=True).decode(str(charset), "ignore").encode('utf8', 'replace')
                text = text + part.get_payload(decode=True).decode(str(charset), "ignore")

        if text is not None:
            return text.strip()
    else:
        # text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
        return text.strip()


def sort_mail(client):
    logger.info("do_work")
    messages = client.search('ALL')
    for uid, message_data in client.fetch(messages, 'RFC822').items():
        uuid = str(uid)
        work_logger = setup_logger(uuid, os.path.join(log_dir, f'{uuid}.log', level=log_level))
        email_message = email.message_from_bytes(message_data[b'RFC822'], policy=policy.default)
        work_logger.debug("RAW EMAIL MASSAGE")
        work_logger.debug(f"email_message.get_content_charset()={email_message.get_content_charset()}")
        work_logger.debug(f"email_message.get_charset()={email_message.get_charset()}")
        work_logger.debug("=" * 45)
        work_logger.debug(email_message)
        work_logger.debug("=" * 45)
        ffrom = email_message.get('From')
        fsubject = email_message.get('Subject')
        work_logger.debug(f"uid={uuid}")
        work_logger.debug(f"ffrom={ffrom}")
        work_logger.debug(f"fsubject={fsubject}")
        body = get_decoded_email_body(email_message)
        work_logger.debug(f"body={body}")


def main():
    # context manager ensures the session is cleaned up
    with IMAPClient(host="imap.yandex.ru", use_uid=True) as client:
        client.login(ymail_login, ymail_password)
        client.select_folder('INBOX')
        # Первый раз просто сканируем почту и делаем работу, а потом переходим в режим ожидания
        sort_mail(client)
        # Start IDLE mode
        client.idle()
        print("Connection is now in IDLE mode, send yourself an email or quit with ^c")
        logger.info("Connection is now in IDLE mode, send yourself an email or quit with ^c")
        while True:
            try:
                # Wait for up to 30 seconds for an IDLE response
                responses = client.idle_check(timeout=60)
                # print(f"Server sent:{responses if responses else 'nothing'}")
                logger.debug(f"Server sent:{responses if responses else 'nothing'}")

                # print(responses)
                # logging.debug("Server sent:", responses if responses else "nothing")
                if responses:
                    sort_mail(client)
            except KeyboardInterrupt:
                break
        client.idle_done()
        print("\nIDLE mode done")
        logger.info("\nIDLE mode done")
        client.logout()


if __name__ == "__main__":
    main()

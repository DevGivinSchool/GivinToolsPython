from imapclient import IMAPClient
import sys
import os
import logging
import email
from email import policy

# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(process)d:%(thread)d - %(message)s')


def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


logger = setup_logger('mail_scaner', 'd:\!SAVE\log\myapp.log')
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


def do_work():
    logger.info("do_work")
    messages = client.search('ALL')
    for uid, message_data in client.fetch(messages, 'RFC822').items():
        uuid = str(uid)
        work_logger = setup_logger(uuid, f'd:\!SAVE\log\{uuid}.log')
        email_message = email.message_from_bytes(message_data[b'RFC822'], policy=policy.default)
        work_logger.info("RAW EMAIL MASSAGE")
        work_logger.info(f"email_message.get_content_charset()={email_message.get_content_charset()}")
        work_logger.info(f"email_message.get_charset()={email_message.get_charset()}")
        work_logger.info("=" * 45)
        work_logger.info(email_message)
        work_logger.info("=" * 45)
        ffrom = email_message.get('From')
        fsubject = email_message.get('Subject')
        work_logger.info(f"uid={uuid}")
        work_logger.info(f"ffrom={ffrom}")
        work_logger.info(f"fsubject={fsubject}")
        body = ""
        body2 = ""
        if email_message.is_multipart():
            work_logger.info("message is multipart")
            for part in email_message.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                # skip any text/plain (txt) attachments
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload()
                    body2 = part.get_payload(decode=True)  # decode
                    break
        else:
            work_logger.info("message is NOT multipart")
            body = email_message.get_payload()
            body2 = email_message.get_payload(decode=True)
        # body.decode("utf-8")
        work_logger.info(f"body={body}")
        work_logger.info(f"body2={body2}")


# context manager ensures the session is cleaned up
with IMAPClient(host="imap.yandex.ru", use_uid=True) as client:
    client.login(ymail_login, ymail_password)
    client.select_folder('INBOX')
    # Первый раз просто сканируем почту и делаем работу, а потом переходим в режим ожидания
    do_work()
    # Start IDLE mode
    client.idle()
    print("Connection is now in IDLE mode, send yourself an email or quit with ^c")
    logger.info("Connection is now in IDLE mode, send yourself an email or quit with ^c")
    while True:
        try:
            # Wait for up to 30 seconds for an IDLE response
            responses = client.idle_check(timeout=60)
            print(f"Server sent:{responses if responses else 'nothing'}")
            logger.info(f"Server sent:{responses if responses else 'nothing'}")

            # print(responses)
            # logging.debug("Server sent:", responses if responses else "nothing")
            if responses:
                do_work()
        except KeyboardInterrupt:
            break
    client.idle_done()
    print("\nIDLE mode done")
    logger.info("\nIDLE mode done")
    client.logout()

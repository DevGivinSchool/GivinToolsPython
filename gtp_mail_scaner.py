"""Mail robot for Givin School. Processes incoming mail and performs tasks transmitted in letters.

    Documentation style Sphinx - `<http://www.sphinx-doc.org/en/1.8/>`_

"""
from imapclient import IMAPClient
import sys
import os
import logging
import email
# from gtp import Task
from Task import Task
from email.header import decode_header

# Variables for logging
log_dir = r"c:\!SAVE\log"
# log_dir = "d:\!SAVE\log"
log_formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(process)d:%(thread)d - %(message)s')
log_level = logging.DEBUG


def setup_logger(name, log_file, level=logging.INFO):
    """Create custom loggers.
    :param str name: Name of logger.
    :param str log_file: File that logger writes to.
    :param level: Logging level.
    :return llogger: The custom logger.
    """
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(log_formatter)
    llogger = logging.getLogger(name)
    llogger.setLevel(level)
    llogger.addHandler(handler)
    return llogger


logger = setup_logger('mail_scaner', os.path.join(log_dir, 'mail_scaner.log'), log_level)
logger.info('START MAIL SCANER')

# Get login and password from envirement
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
    """Decode email body.
    Detect character set if the header is not set. We try to get text/plain.
    :param msg: Raw 7-bit message body input e.g. from imaplib.
    :return: Body of the letter in the desired encoding
    """

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

        return text.strip()
    else:
        # text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
        text = msg.get_payload(decode=True).decode(msg.get_content_charset(), 'ignore')
        return text.strip()


def string_normalization(msg):
    return msg.strip().lstrip("<").rstrip(">")


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


def sort_mail(client):
    """Sort mail and start baground jobs.
    For each letter run job in the background.
    :param IMAPClient client: IMAPClient instance.
    """
    logger.info("do_work")
    messages = client.search('ALL')
    for uid, message_data in client.fetch(messages, 'RFC822').items():
        uuid = str(uid)
        work_logger = setup_logger(uuid, os.path.join(log_dir, f'{uuid}.log'), log_level)
        email_message = email.message_from_bytes(message_data[b'RFC822'])
        work_logger.debug("RAW EMAIL MASSAGE")
        work_logger.debug(f"email_message.get_content_charset()={email_message.get_content_charset()}")
        work_logger.debug(f"email_message.get_charset()={email_message.get_charset()}")
        work_logger.debug("=" * 45)
        work_logger.debug(email_message)
        work_logger.debug("=" * 45)
        work_logger.debug(f"uid={uuid}")
        work_logger.debug(f"raw_ffrom=|{email_message.get('From')}|")
        work_logger.debug(f"raw_fsubject=|{email_message.get('Subject')}|")
        ffrom = string_normalization(get_decoded_str(email_message.get('From')))
        # fsubject = email_message.get('Subject')
        fsubject = get_decoded_str(email_message.get('Subject'))
        work_logger.debug(f"ffrom={ffrom}")
        work_logger.debug(f"fsubject={fsubject}")
        body = get_decoded_email_body(email_message)
        work_logger.debug(f"body={body}")
        k = Task(uuid, ffrom, fsubject, body, work_logger)
        k.display_task()


def main():
    """Main.
    Check mailbox and execute sort_mail() then go to idle mode for IMAPClient.
    And every time if mail server return anything - execute sort_mail().
    """
    with IMAPClient(host="imap.yandex.ru", use_uid=True) as client:
        client.login(ymail_login, ymail_password)
        client.select_folder('INBOX')
        # First sort_mail() execution then go to idle mode
        sort_mail(client)
        # Start IDLE mode
        client.idle()
        print("Connection is now in IDLE mode, send yourself an email or quit with ^c")
        logger.info("Connection is now in IDLE mode, send yourself an email or quit with ^c")
        while True:
            try:
                # Wait for up to XX seconds for an IDLE response
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


logger.info('END MAIL SCANER')

if __name__ == "__main__":
    main()

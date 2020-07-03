#!/home/robot/MyGit/GivinToolsPython/venv/bin/python3.8
import PASSWORDS
import traceback
import sys
import custom_logger
import os
from datetime import datetime
from imapclient import IMAPClient
from Class_Email import Email
from alert_to_mail import send_mail


if __name__ == "__main__":
    program_file = os.path.realpath(__file__)
    logger = custom_logger.get_logger(program_file=program_file)
    logger.info('START gtp_school_friends')
    try:
        client = IMAPClient(host="imap.yandex.ru", use_uid=True)
        client.login(PASSWORDS.settings['ymail_login'], PASSWORDS.settings['ymail_password'])
        # Список папко
        # print(client.list_folders())
        """
        [((b'\\Unmarked', b'\\HasNoChildren', b'\\Drafts'), b'|', 'Drafts'),
        ((b'\\Unmarked', b'\\NoInferiors'), b'|', 'INBOX'),
        ((b'\\Unmarked', b'\\HasNoChildren'), b'|', 'Outbox'),
        ((b'\\Unmarked', b'\\HasNoChildren'), b'|', 'Queue'),
        ((b'\\Unmarked', b'\\HasNoChildren', b'\\Sent'), b'|', 'Sent'),
        ((b'\\Unmarked', b'\\HasNoChildren', b'\\Junk'), b'|', 'Spam'),
        ((b'\\Unmarked', b'\\HasNoChildren', b'\\Trash'), b'|', 'Trash')]
        """
        client.select_folder('INBOX')
        logger.info('Connect Yandex server successful')
    except Exception:
        client.logout()
        error_text = "MAIN ERROR (Yandex mail):\n" + traceback.format_exc()
        print(error_text)
        logger.error(error_text)
        logger.error(f"Send email to: {PASSWORDS.settings['admin_emails']}")
        send_mail(PASSWORDS.settings['admin_emails'], "MAIN ERROR (Yandex mail)", error_text, logger,
                  attached_file=logger.handlers[0].baseFilename)
        logger.error("Exit with error")
        sys.exit(1)
    # First sort_mail() execution then go to idle mode
    email = Email(client, logger)
    email.sort_mail()
    client.logout()
    logger.info('END gtp_school_friends')

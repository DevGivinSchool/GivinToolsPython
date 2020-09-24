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
from Class_DBPostgres import DBPostgres
from alert_to_mail import raise_error


if __name__ == "__main__":
    program_file = os.path.realpath(__file__)
    logger = custom_logger.get_logger(program_file=program_file)
    logger.info('START gtp_school_friends')
    try:
        logger.info("Try connect to DB")
        postgres = DBPostgres(dbname=PASSWORDS.settings['postgres_dbname'], user=PASSWORDS.settings['postgres_user'],
                              password=PASSWORDS.settings['postgres_password'],
                              host=PASSWORDS.settings['postgres_host'],
                              port=PASSWORDS.settings['postgres_port'], logger=logger)
    except Exception:
        raise_error("ERROR: Postgres connect", logger, prog_name="Class_Email.py")
        sys.exit(1)
    sql_text = """INSERT INTO sessions(time_begin, log) VALUES (NOW(), %s) RETURNING id;"""
    values_tuple = (logger.handlers[0].baseFilename,)
    session_id = postgres.execute_dml_id(sql_text, values_tuple)
    logger.info(f'Session begin (session_id={session_id})')
    logger.info('#' * 45)
    try:
        client = IMAPClient(host="imap.yandex.ru", use_uid=True)
        client.login(PASSWORDS.settings['ymail_login'], PASSWORDS.settings['ymail_password'])
        # Список папко
        # print(client.list_folders())
        """
        [((b'\\HasNoChildren', b'\\Marked'), b'|', 'Archive'),
         ((b'\\HasNoChildren', b'\\Unmarked', b'\\Drafts'), b'|', 'Drafts'),
         ((b'\\HasNoChildren', b'\\Unmarked', b'\\NoInferiors'), b'|', 'INBOX'),
         ((b'\\HasNoChildren', b'\\Marked'), b'|', 'Notification'),
         ((b'\\HasNoChildren', b'\\Unmarked'), b'|', 'Outbox'),
         ((b'\\HasNoChildren', b'\\Unmarked', b'\\Sent'), b'|', 'Sent'),
         ((b'\\HasNoChildren', b'\\Unmarked', b'\\Junk'), b'|', 'Spam'),
         ((b'\\HasNoChildren', b'\\Marked', b'\\Trash'), b'|', 'Trash')]
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
    email = Email(client, postgres, session_id, logger)
    email.sort_mail()
    client.logout()
    postgres.session_end(session_id)
    logger.info('#' * 45)
    logger.info(f'Session end')
    logger.info('END gtp_school_friends')

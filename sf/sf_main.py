#!/home/robot/MyGit/GivinToolsPython/venv/bin/python3.8
import core.PASSWORDS as PASSWORDS
import traceback
import sys
import core.custom_logger as custom_logger
import os
# from datetime import datetime
from imapclient import IMAPClient
from sf.Class_Email import Email
from core.alert_to_mail import send_mail, raise_error
from core.Class_DBPostgres import DBPostgres

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
    email = Email(client, postgres, session_id, logger)
    email.sort_mail()
    client.logout()
    postgres.session_end(session_id)
    logger.info('#' * 45)
    logger.info(f'Session end')
    logger.info('END gtp_school_friends')

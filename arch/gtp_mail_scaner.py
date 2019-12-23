"""Mail robot for Givin School. Processes incoming mail and performs tasks transmitted in letters.

    Documentation style Sphinx - `<http://www.sphinx-doc.org/en/1.8/>`_

"""
from imapclient import IMAPClient
import sys
import os
from Log import Log
from test.Email import Email
import logging

log_level = logging.DEBUG


def get_login(logger):
    global ymail_login, ymail_password
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


def main():
    """Main.
    Check mailbox and execute sort_mail() then go to idle mode for IMAPClient.
    And every time if mail server return anything - execute sort_mail().
    """
    Log.LEVEL = logging.DEBUG
    logger = Log.setup_logger('mail_scaner', 'mail_scaner.log')
    logger.info('START MAIL SCANER')

    get_login(logger)

    with IMAPClient(host="imap.yandex.ru", use_uid=True) as client:
        client.login(ymail_login, ymail_password)
        client.select_folder('INBOX')
        # First sort_mail() execution then go to idle mode
        email = Email(client, logger)
        email.sort_mail()
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
                    email.sort_mail()
            except KeyboardInterrupt:
                break
        client.idle_done()
        print("\nIDLE mode done")
        logger.info("\nIDLE mode done")
        client.logout()

    logger.info('END MAIL SCANER')


if __name__ == "__main__":
    main()

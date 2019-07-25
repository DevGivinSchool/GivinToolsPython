from imapclient import IMAPClient
import PASSWORDS
import sys
import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    level=logging.DEBUG,
    filename='d:\!SAVE\log\myapp.log',
    filemode='w'
)
"""
logger = logging.getLogger('my_app')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('d:\!SAVE\log\myapp.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
"""

def save_mail_to_disk():
    print("save_mail_to_disk")
    logging.debug("save_mail_to_disk")

# context manager ensures the session is cleaned up
with IMAPClient(host="imap.yandex.ru", use_uid=True) as client:
    client.login(ymail_login, ymail_password)
    client.select_folder('INBOX')

    # Start IDLE mode
    client.idle()
    print("Connection is now in IDLE mode, send yourself an email or quit with ^c")
    logging.debug("Connection is now in IDLE mode, send yourself an email or quit with ^c")

    while True:
        try:
            # Wait for up to 30 seconds for an IDLE response
            responses = client.idle_check(timeout=10)
            print(f"Server sent:{responses if responses else 'nothing'}")
            logging.debug(f"Server sent:{responses if responses else 'nothing'}")

            #print(responses)
            #logging.debug("Server sent:", responses if responses else "nothing")
            if responses:
                print("Процедура сохранения писем")
                logging.debug("Процедура сохранения писем")
                save_mail_to_disk()

        except KeyboardInterrupt:
            break
    client.idle_done()
    print("\nIDLE mode done")
    logging.debug("\nIDLE mode done")
    client.logout()

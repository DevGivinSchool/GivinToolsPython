import smtplib
import ssl
import traceback

import PASSWORDS
import logging

logger = logging.getLogger('alert_to_mail')


def send_mail(receiver_emails, subject, message, sender_email="robot@givinschool.org", port=465):
    logger.info(f"Send email to {receiver_emails}")
    print(f"LOGGER = {logger}")
    # Create a secure SSL context
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context)
    try:
        server.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
    except Exception:
        logger.error("ERROR: Can't connect to SMTP server:\n" + traceback.format_exc())
    try:
        mail_text = "\r\n".join((
            "From: %s" % sender_email,
            "To: %s" % receiver_emails,
            "Subject: %s" % subject,
            "",
            message
        ))
        server.sendmail(sender_email, receiver_emails, mail_text)
    except Exception:
        logger.error(f"ERROR: Can't send email to {receiver_emails}:\n" + traceback.format_exc())
    server.quit()


if __name__ == "__main__":
    mail_to = PASSWORDS.logins['admin_emails']
    SUBJECT = "Test email from Python"
    FROM = "robot@givinschool.org"
    text = "Python 3.4 rules them all!"

    msg = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % mail_to,
        "Subject: %s" % SUBJECT,
        "",
        text
    ))
    send_mail(FROM, mail_to, msg)

import smtplib
import ssl
import PASSWORDS
import logging

logger = logging.getLogger('alert_to_mail')


def send_mail(receiver_email, message, sender_email="robot@givinschool.org", port=465):
    logger.info(f"Send email to {receiver_email}")
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context)
        server.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
    except Exception as e:
        logger.info("ERROR: Can't connect to SMTP server")
    try:
        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        logger.info(f"ERROR: Can't send email to {receiver_email}")
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
    send_mail(mail_to, msg)

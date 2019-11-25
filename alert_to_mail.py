import smtplib
import ssl
import traceback
import PASSWORDS
import logging
from email.mime.text import MIMEText
from email.header import Header

logger = logging.getLogger('alert_to_mail')


def send_mail(receiver_emails, subject, message, sender_email="robot@givinschool.org", port=465):
    """
    Отправка почтового сообщения
    :param list receiver_emails: Список email получателей
    :param str subject: Тема письма
    :param str message: Тело письма
    :param str sender_email: Адрес email отправителя
    :param int port: Порт
    :return:
    """
    logger.info(f"Send email to {receiver_emails}")
    print(f"LOGGER = {logger}")
    # Create message
    email_text = MIMEText(message, 'plain', 'utf-8')
    email_text['Subject'] = Header(subject, 'utf-8')
    email_text['From'] = sender_email
    email_text['To'] = receiver_emails
    # Create a secure SSL context
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context)
    try:
        server.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
    except Exception:
        logger.error("ERROR: Can't connect to SMTP server:\n" + traceback.format_exc())
    try:
        server.sendmail(sender_email, receiver_emails, email_text.as_string())
    except Exception:
        logger.error(f"ERROR: Can't send email to {receiver_emails}:\n" + traceback.format_exc())
    server.quit()


if __name__ == "__main__":
    mail_text = f"Создать учётку zoom участнику Иванов " \
                f"Иван\nLogin: ivanov_ivan@givinschool.org\nPassword: X2#FQDIcur"
    send_mail(PASSWORDS.logins['admin_emails'], "CREATE ZOOM", mail_text)

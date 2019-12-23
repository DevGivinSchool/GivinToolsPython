import smtplib
import ssl
import traceback
import PASSWORDS
from email.mime.text import MIMEText
from email.header import Header


def send_mail(receiver_emails, subject, message, logger, sender_email="robot@givinschool.org", port=465):
    """
    Отправка почтового сообщения
    :param list receiver_emails: Список email получателей
    :param str subject: Тема письма
    :param str message: Тело письма
    :param str sender_email: Адрес email отправителя
    :param int port: Порт
    :return:
    """
    # Create a secure SSL context
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context)
    try:
        server.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
    except Exception:
        logger.error("ERROR: Can't connect to SMTP server:\n" + traceback.format_exc())
    for one_receiver in receiver_emails:
        logger.info(f"Send email to {one_receiver}")
        # print(f"LOGGER = {logger}")
        print(f"Send email to {one_receiver}")
        # Create message
        email_text = MIMEText(message, 'plain', 'utf-8')
        email_text['Subject'] = Header(subject, 'utf-8')
        email_text['From'] = sender_email
        email_text['To'] = one_receiver
        try:
            server.sendmail(sender_email, one_receiver, email_text.as_string())
        except Exception:
            logger.error(f"ERROR: Can't send email to {one_receiver}:\n" + traceback.format_exc())
    server.quit()


if __name__ == "__main__":
    mail_text = f"Создать учётку zoom участнику Иванов " \
                f"Иван\nLogin: ivanov_ivan@givinschool.org\nPassword: X2#FQDIcur"
    send_mail(PASSWORDS.logins['admin_emails'], "CREATE ZOOM", mail_text)

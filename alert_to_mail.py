import os
import smtplib
import ssl
import traceback
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import PASSWORDS
import log_config
from email.mime.text import MIMEText
from email.header import Header
from Log import Log


def send_mail(receiver_emails, subject, message, logger, attached_file=None, sender_email="robot@givinschool.org", port=465):
    """
    Отправка почтового сообщения
    :param logger: Логгер
    :param attached_file: Пусть к файлу вложения (по умолчанию None - без вложения)
    :param list receiver_emails: Список email получателей
    :param str subject: Тема письма
    :param str message: Тело письма
    :param str sender_email: Адрес email отправителя
    :param int port: Порт
    :return:
    """
    logger.info(f"Отправка почтовых оповещений")
    # Все письма отправляются на почту robot для хранения.
    if PASSWORDS.logins['ymail_login'] not in receiver_emails:
        receiver_emails.append(PASSWORDS.logins['ymail_login'])
    # Create a secure SSL context
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context)
    # Try connect to server
    try:
        server.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
    except Exception:
        logger.error("ERROR: Can't connect to SMTP server:\n" + traceback.format_exc())
    # Partial create message (without To)
    # msg = MIMEText(message, 'plain', 'utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender_email
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    if attached_file is not None:
        attachment = open(attached_file, 'rb')
        xlsx = MIMEBase('application', 'vnd.ms-excel')
        # xlsx = MIMEBase('application', 'octet-stream')
        # xlsx = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        xlsx.set_payload(attachment.read())
        attachment.close()
        encoders.encode_base64(xlsx)
        xlsx.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attached_file))
        msg.attach(xlsx)
    logger.info(f"Список адресов: {receiver_emails}")
    for one_receiver in receiver_emails:
        # print(f"Send email to {one_receiver}")
        # logger.info(f"Send email to {one_receiver}")
        # print(f"LOGGER = {logger}")
        msg['To'] = one_receiver
        try:
            server.sendmail(sender_email, one_receiver, msg.as_string())
        except Exception:
            logger.error(f"ERROR: Can't send email to {one_receiver}:\n" + traceback.format_exc())
    server.quit()


if __name__ == "__main__":
    logger = Log.setup_logger('__main__', log_dir, f'gtp_alert_to_mail.log',
                              log_level)
    """mail_text = f"Создать учётку zoom участнику Иванов " \
                f"Иван\nLogin: ivanov_ivan@givinschool.org\nPassword: X2#FQDIcur"
    send_mail(PASSWORDS.logins['admin_emails'], "CREATE ZOOM", mail_text)"""
    name = "ДМИТРИЙ"
    login = "bbbbb_ddsgqwawe@givinschool.org"
    password = "V4$mWEXCqr"
    mail_text2 = f"""Здравствуйте, {name.title()}!  

Поздравляем, Вы оплатили абонемент на месяц совместных занятий в онлайн-формате "Друзья Школы Гивина". 

Ваш новый zoom-аккаунт:
Логин: {login}
Пароль: {password}

Сохраните себе эти данные, чтобы не потерять их. 

Эти данные вы можете использовать с настоящего момента:
1) Скачайте приложение Zoom на компьютер, если ещё не cделали это ранее. 
2) Установите приложение Zoom на ваш компьютер.
3) Запустите эту программу.
4) Нажмите кнопку Sign In ("Войти в..").
5) Введите логин и пароль, предоставленные вам в этом письме .
6) Поставьте птичку (галку) в поле Keep me logged in ("Не выходить из системы").
7) Нажмите Sign In ("Войти"). 
8) Далее из чата Объявлений в телеграмме найдет сообщение с ссылкой на занятия. Нажмите на неё. Она будет открываться в браузере, появится сверху сообщение с кнопкой, жмём на кнопку Open ZOOM Meetings (либо Открыть ZOOM)
9) Появится окно для ввода пароля конференции. Здесь вводим три цифры 355. 

С благодарностью и сердечным теплом,
команда Школы Гивина."""
    send_mail(PASSWORDS.logins['admin_emails'],
              r"[ШКОЛА ГИВИНА]. Поздравляем, Вы приняты в Друзья Школы", mail_text2, logger)

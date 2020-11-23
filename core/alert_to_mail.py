import os
import smtplib
import ssl
import traceback
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import core.PASSWORDS as PASSWORDS
from email.mime.text import MIMEText
from email.header import Header


def send_mail(receiver_emails, subject, message, logger, attached_file=None,
              sender_email="robot@givinschool.org", port=465):
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
    logger.debug(">>>>alert_to_mail.send_mail begin")
    logger.info("Отправка почтовых оповещений")
    # Все письма отправляются на почту robot для хранения.
    if PASSWORDS.settings['ymail_login'] not in receiver_emails:
        receiver_emails.append(PASSWORDS.settings['ymail_login'])
    # Create a secure SSL context
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context)
    # Try connect to server
    try:
        server.login(PASSWORDS.settings['ymail_login'], PASSWORDS.settings['ymail_password'])
    except Exception:
        logger.error("ERROR: Can't connect to SMTP server:\n" + traceback.format_exc())
    # Partial create message (without To)
    # msg = MIMEText(message, 'plain', 'utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender_email
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    if attached_file is not None:
        attached_file_name = os.path.basename(attached_file)
        logger.info(f"Вложение: {attached_file_name}")
        attachment = open(attached_file, 'rb')
        xlsx = MIMEBase('application', 'vnd.ms-excel')
        # xlsx = MIMEBase('application', 'octet-stream')
        # xlsx = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        xlsx.set_payload(attachment.read())
        attachment.close()
        encoders.encode_base64(xlsx)
        xlsx.add_header('Content-Disposition', 'attachment', filename=attached_file_name)
        msg.attach(xlsx)
    else:
        logger.info("Вложение: НЕТ")
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
    logger.debug(">>>>alert_to_mail.send_mail end")


def send_error_to_admin(subject, logger, prog_name="NONE"):
    """
    Логировать сообщение об ошибке, вывод его на консоль, отослать его на email администратору.
    :param subject: Тема письма
    :return:
    """
    if not prog_name:
        prog_name = os.path.basename(logger.handlers[0].baseFilename.split(".")[0])
    subject = f"[ERROR][{prog_name}]:{subject}"
    error_text = f"{subject}:\n" + traceback.format_exc()
    print(error_text)
    logger.error(error_text)
    logger.info(f"Send email to: {PASSWORDS.settings['admin_emails']}")
    attached_file = logger.handlers[0].baseFilename
    send_mail(PASSWORDS.settings['admin_emails'], subject, error_text, logger, attached_file=attached_file)


def raise_error(err_text_, logger_, prog_name="NONE"):
    """
    Делает всё тоже что и send_error_to_admin + генерация исключения.
    Делать ли выход из приложения (exit(1)) после генерации исключения, определяется в коде
    :param err_text_: Текст ошибки
    :param logger_: логгер
    """
    send_error_to_admin(err_text_, logger_, prog_name=prog_name)
    raise Exception(err_text_)


def get_participant_notification_text(last_name, first_name, login, password):
    mail_text2 = f"""Здравствуйте, {last_name.capitalize()} {first_name.capitalize()}!  

Поздравляем, Вы оплатили абонемент для совместных занятий в онлайн-формате "Друзья Школы Гивина". 

Ваш zoom-аккаунт:
Логин: {login}
Пароль: {password}

Сохраните себе эти данные, чтобы не потерять их. 

Эти данные вы можете использовать с настоящего момента:
1) Скачайте приложение Zoom на компьютер, если ещё не cделали это ранее. 
2) Установите приложение Zoom на ваш компьютер.
3) Запустите эту программу.
4) Нажмите кнопку Sign In ("Войти в..").
5) Введите логин и пароль, предоставленные вам в этом письме.
6) Поставьте птичку (галку) в поле Keep me logged in ("Не выходить из системы").
7) Нажмите Sign In ("Войти"). 
8) Далее из чата Объявлений в телеграмме найдет сообщение с ссылкой на занятия. Нажмите на неё.
   Она будет открываться в браузере, появится сверху сообщение с кнопкой,
   жмём на кнопку Open ZOOM Meetings (либо Открыть ZOOM).

С благодарностью и сердечным теплом,
команда Школы Гивина."""
    return mail_text2


if __name__ == "__main__":
    # print(get_participant_notification_text("fam", "mane", "xxx@givinschool.org", "passwd"))
    import core.custom_logger as custom_logger

    program_file = os.path.realpath(__file__)
    logger = custom_logger.get_logger(program_file=program_file)

    receiver_emails = PASSWORDS.settings['admin_emails']
    subject = "DEBUG: alert_to_mail.py"
    message = "DEBUG: alert_to_mail.py"
    # attached_file = None
    attached_file = logger.handlers[0].baseFilename
    send_mail(receiver_emails, subject, message, logger, attached_file)

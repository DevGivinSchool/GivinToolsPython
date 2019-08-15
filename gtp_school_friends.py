"""
#### В случае любой ошибки отослать письмо админам
Подключение логирования
Считывание настроек программы
Подключаюсь к почте robot@givinschool.org
Выбираю письма от noreply@server.paykeeper.ru и от no-reply@getcourse.ru
Обрабатываю эти письма:
    Это нужное письмо?
        Да (это платёж):
           Проверяю новый ли это пользователь:
              Если новый:
                  Транслитерация ФИО
                  Генерация пароля
                  Завожу ему почту Яндекс
                  Завожу ему учётку Zoom
                  Отсылаю ему письмо о регистрации
                  Отсылаю ему сообщение Телеграм о регистрации
                  --Отмечаю в GetCourse (=меняю примечание к заказу)
              Если старый:
                  Проверяю заблокирован ли он:
                      Если заблокирован:
                          Возвращаю пароль zoom на место
                          Отмечаю дату оплаты
                          Отмечаю разблокировку
                          Отсылаю ему письмо о разблокировке
                          Отсылаю ему сообщение Телеграм о разблокировке
                      Если не заблокирован:
                          Отмечаю дату оплаты
                          Отсылаю ему письмо о продлении
                          Отсылаю ему сообщение Телеграм о продлении
            Переместить письмо в папку Friends
        Нет (это нужное письмо с темой:)
            Тема sf --add --new:
                Процедура добавления совсем нового пользователя
            Тема sf --block:
                Процедура блокировки пользователя
            Тема sf --checkin:
                Процедура отмечания оплаты пользователем
            Тема sf --report --type XXX --intend XXX --sdate 01.01.1900 --edate 01.01.1900 --month N:
                Процедура получения различных выгрузок данных в виде .csv файлов
        Нет (это не нужное письмо, не платёж):
            Удаляю это письмо в корзину
Процедура проверки просрочки (проверяю временно интервал 10-11 часов + отметка о том что письмо уже было отправлено)
    Время между 10 и 11 + письмо не отсылалось еще?
        Да:
            Получить список тех у кого просрочка более 30 дней:
                Список отослать менеджерам (Павлу) по почте или Телеграм
"""

from Log import Log
import logging
import os
import config
from imapclient import IMAPClient
import PASSWORDS
from Email2 import Email
from datetime import datetime

# Текущая дата для имени лог файла (без %S)
now = datetime.now().strftime("%Y%m%d%H%M")
logger = Log.setup_logger('__main__', config.config['log_dir'], f'gtp_school_friends_{now}.log', config.config['log_level'])
logger.info('START gtp_school_friends')


def main():

    with IMAPClient(host="imap.yandex.ru", use_uid=True) as client:
        client.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
        client.select_folder('INBOX')
        # First sort_mail() execution then go to idle mode
        email = Email(client, logger)
        email.sort_mail()
        client.logout()

    logger.info('END gtp_school_friends')


if __name__ == "__main__":
    main()

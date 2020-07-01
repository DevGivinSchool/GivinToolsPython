#!/home/robot/MyGit/GivinToolsPython/venv/bin/python3.8

# TODO Процедуру проверки суммы оплаты нужно изменить под ставку 1990 за месяц + сумма на одностраничниках.
#      Есть кто платит за 2 месяца - этого нет сейчас в проверке и на одностраничниках.

# Здесь есть полезные фишки для БД - https://github.com/alexey-goloburdin/telegram-finance-bot/blob/master/expenses.py

# TODO процедуру блокировки пользователя Zoom вставить в sf_daily_works.py.

# TODO В этом заказе ник Телеграм в поле - Ник телеграмм, нужно в парсинге это учесть. 

# TODO Когда парсим страницу, нужно почту и телеграм вносить в БД если их там нет
#  - это только для старых пользователей в этом месте, после self.mark_payment_into_db() новую процедуру

# TODO Если срок платежа не закончился то нужно прибавлять эти дни.
# TODO Написать текст сообщение по правилам заполнения полей при оплате в чат Телеграм ДШ
# TODO Еще возможно проецдура заморозки участия, т.е. сейчас человек оплатил, но участвовать не может.
#      его нужно заблокировать сейчас, а потом по требованию разблокировать с переносом даты окончания срока,
#      дату отплаты трогать не нужно + добавить коментарий что он разморожен.

# TODO Для GetCourse проверять если это платёж не за ДШ, но сумма 1990р - писать warning в лог.
# TODO Процедура блокирования участников (пока ручной запуск)

# TODO Процедуру проверки всех почт с которых могу приходить письма. 
#      Если адреса нет в общем списке тогда слать админу письмо что появилась какая-то незнакомая почта

# TODO Оповещение админов о работах по почте c вложением логов

# TODO Сделать почтового бота. How to Make a Python Email Bot -
#  https://repl.it/talk/learn/How-to-Make-a-Python-Email-Bot/8194/20686

# TODO Оповещение пользователей в Телеграм
# TODO Оповещение админов о работах в Телеграм
# TODO Процедура обработки писем с командами (fsubject.startswith("#"))

# TODO Процедура - поменять местами имя и фамилию в БД и для eng тоже (для новеньких). Некоторые путают при регистрации.

# TODO Отправка писем через IMAP robot, чтобы письма сохранялись. Это гиморой.
#  Поэтому лучше сделать динамически получать текст письма с помощью данных из БД.


"""
#### В случае любой ошибки отослать письмо админам
Подключение логирования
Считывание настроек программы
Подключаюсь к почте robot@givinschool.org
Выбираю письма от noreply@server.paykeeper.ru и от no-reply@getcourse.ru
DB: Создаю сессию работы
Обрабатываю эти письма:
    TRY: Если при обработке одной задачи происходит ошибка - записываю ошибку в БД и иду дальше.
        DB: Создаю задачу (для каждого письма своя задача)
            ЕСЛИ: Такая задача уже есть, увеличиваю счётчик попыток.
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
        DB: Закрываю задачу
DB: Закрываю сессию работы
Процедура проверки просрочки (проверяю временно интервал 10-11 часов + отметка о том что письмо уже было отправлено)
    Время между 10 и 11 + письмо не отсылалось еще?
        Да:
            Получить список тех у кого просрочка более 30 дней:
                Список отослать менеджерам (Павлу) по почте или Телеграм
"""
import PASSWORDS
import traceback
import sys
import custom_logger
import os
from datetime import datetime
from imapclient import IMAPClient
from Class_Email import Email
from alert_to_mail import send_mail


if __name__ == "__main__":
    program_file = os.path.realpath(__file__)
    logger = custom_logger.get_logger(program_file=program_file)
    logger.info('START gtp_school_friends')
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
        # TODO Вынести процедуру опопвещения MAIN ERROR в отдельную процедуру
        error_text = "MAIN ERROR (Yandex mail):\n" + traceback.format_exc()
        print(error_text)
        logger.error(error_text)
        logger.error(f"Send email to: {PASSWORDS.settings['admin_emails']}")
        send_mail(PASSWORDS.settings['admin_emails'], "MAIN ERROR (Yandex mail)", error_text, logger,
                  attached_file=logger.handlers[0].baseFilename)
        logger.error("Exit with error")
        sys.exit(1)
    # First sort_mail() execution then go to idle mode
    email = Email(client, logger)
    email.sort_mail()
    # TODO Процедура чистки: 1) Удалять всех заблокированных пользователей больше года
    client.logout()
    logger.info('END gtp_school_friends')

# TODO В процедуре учёти платежа mark_payment_into_db нужно учитывать type, если B - тогда нужно пароль на Zoom менять

# TODO Написать текст сообщение по правилам заполнения полец при оплате в чат Телеграм ДШ

# TODO Для GetCourse проверять если это платёж не за ДШ, но сумма 1990р - писать warning в лог.
# TODO Процедура блокирования участников (пока ручной запуск)
# TODO Сведения об участнике в лог

# TODO Если body_type = html тогда преобразовывать его в простой текст перед записью в лог

# TODO Временно можно создавать пользователей GetCourse без почты - писать в лог WARNING
# TODO Нового пользователя создавать с type='N' после первой оплати ему проставиться 'P'

# TODO Из писем Геткурc получать ссылку на заказ
#      Страница заказ: https://givinschoolru.getcourse.ru/sales/control/deal/update/id/20860383
# TODO Парсинг ссылки на заказ из Геткурс = Написать на все форумы

# TODO Оповещение пользователей по почте ни основе шаблона
# TODO Оповещение админов о работах по почте c вложением логов

# TODO Получение списка должников и его отправка менедджерам по почте
#  (пока вручную запросом и потом через выгрузку в TXT и в Excel)
#     в этот список включать пользователей без почты и телеграм

# TODO Сделать почтового бота. How to Make a Python Email Bot -
#  https://repl.it/talk/learn/How-to-Make-a-Python-Email-Bot/8194/20686

# TODO Оповещение пользователей в Телеграм
# TODO Оповещение админов о работах в Телеграм

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
from Log import Log
import config
import PASSWORDS
import traceback
import sys
from datetime import datetime
from imapclient import IMAPClient
from Email2 import Email
from alert_to_mail import send_mail


# Текущая дата для имени лог файла (без %S)
now = datetime.now().strftime("%Y%m%d%H%M")
logger = Log.setup_logger('__main__', config.config['log_dir'], f'gtp_school_friends_{now}.log',
                          config.config['log_level'])
logger.info('START gtp_school_friends')


def main():
    try:
        client = IMAPClient(host="imap.yandex.ru", use_uid=True)
        client.login(PASSWORDS.logins['ymail_login'], PASSWORDS.logins['ymail_password'])
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
        logger.error(f"Send email to: {PASSWORDS.logins['admin_emails']}")
        send_mail(PASSWORDS.logins['admin_emails'], "MAIN ERROR (Yandex mail)", error_text)
        logger.error("Exit with error")
        sys.exit(1)
    # First sort_mail() execution then go to idle mode
    email = Email(client, logger)
    email.sort_mail()
    # TODO Процедура выявления и оповещения должников.  За 7 и 3 дня отправлять оповещения о необходимости оплаты.
    # TODO Процедура чистки: 1) Удалять всех заблокированных пользователей больше года
    client.logout()
    logger.info('END gtp_school_friends')


if __name__ == "__main__":
    main()

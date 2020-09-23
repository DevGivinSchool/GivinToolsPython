import yandex_mail
import yandex_connect
import payment_creater
import traceback
import PASSWORDS
import sys
# import password_generator
from Class_ZoomUS import ZoomUS
from Class_DBPostgres import DBPostgres
from alert_to_mail import send_mail, get_participant_notification_text
from utils import get_login
from password_generator_for_sf import password_for_sf
from datetime import datetime


class MailMessage:
    """Класс email сообщения"""
    __slots__ = ('subject', 'text')

    def __init__(self, subject, text):
        self.subject = subject
        self.text = text


def select_payment(task_uuid, database):
    sql_text = 'SELECT * FROM payments where task_uuid=%s;'
    values_tuple = (task_uuid,)
    rows = database.execute_select(sql_text, values_tuple)
    return rows


def select_participant(participant_id, database):
    sql_text = 'SELECT * FROM participants where id=%s;'
    values_tuple = (participant_id,)
    rows = database.execute_select(sql_text, values_tuple)
    return rows


def mark_payment_into_db(payment, database, logger, participant_type='P'):
    """
    Отмечаем оплату в БД. Поля until_date (отсрочка до) и comment - обнуляются.
    :return:
    """
    logger.info(">>>> mark_payment_into_db begin")
    mm = MailMessage("", "")
    # Состояние участника до отметки
    # logger.info(select_participant(payment["participant_id"], database))
    # Коментарий и поле отсрочки обнуляются
    # Для заблокированного пользователя меняется его тип (type) и из пароля удаляются два последних символа
    if payment["participant_type"] == "B":
        # Нужно дополнить сведения участника которых не хватает (т.к. это не новый участник а заблокированный)
        result = database.get_participant_by_id(payment["participant_id"])[0]
        payment["Фамилия"] = result[0]
        payment["Имя"] = result[1]
        payment["Фамилия Имя"] = result[2]
        payment["Электронная почта"] = result[3]
        payment["telegram"] = result[4]
        payment["login"] = result[5]
        payment["password"] = result[6]
        # [('ИВАНОВ', 'ИВАН', 'ИВАНОВ ИВАН', 'xxx@mail.ru', '@xxxx', 'ivanov_ivan@givinschool.org', '43RFji1r48')]
        # Исправление пароля (вырезать 55 в конце)
        if payment["password"][-2:] == "55":
            payment["password"] = payment["password"][:-2]
        logger.info("Изменение статуса учатника в БД")
        sql_text = """UPDATE participants 
        SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type=%s, password=%s
        WHERE id=%s;"""
        values_tuple = (payment["Время проведения"], payment["number_of_days"],
                        payment["deadline"], participant_type, payment["password"], payment["participant_id"])
        database.execute_dml(sql_text, values_tuple)
        logger.info("Статус учатника в БД изменён")
        # Измение статуса в zoom
        logger.info("Активация участника в Zoom")
        zoom_user = ZoomUS(logger)
        zoom_result = zoom_user.zoom_users_userstatus(payment["login"], "activate")
        if zoom_result is not None:
            logger.error("+" * 60)
            mail_text = f"\nПроцедура не смогла автоматически разблокировать участника. Ошибка:\n" \
                        f"{zoom_result}" \
                        f"ID={payment['participant_id']}\n{payment['Фамилия Имя']}:" \
                        f"\nLogin: {payment['login']}\nPassword: {payment['password']}"
            send_mail(PASSWORDS.settings['admin_emails'], "UNBLOCK PARTICIPANT ERROR", mail_text, logger)
            logger.error(mail_text)
            logger.error("+" * 60)
        else:
            logger.info("Участник активирован в Zoom")
        # Уведомление участника
        logger.info("Уведомление участника")
        notification_text = participant_notification(payment, r"[ШКОЛА ГИВИНА]. Ваша учтёная запись в Друзьях Школы разблокирована.", logger)
        mm.subject = "[ДШ] РАЗБЛОКИРОВКА УЧАСТНИКА"
        mm.text += "Текст уведомления:\n\n\n" + notification_text
    else:
        logger.info("Отмечаем оплату в БД")
        logger.debug(f"Время проведения|{type(payment['Время проведения'])}|{payment['Время проведения']}")
        logger.debug(f"number_of_days|{type(payment['number_of_days'])}|{payment['number_of_days']}")
        logger.debug(f"deadline|{type(payment['deadline'])}|{payment['deadline']}")
        logger.debug(f"until_date|{type(payment['until_date'])}|{payment['until_date']}")
        sql_text = """UPDATE participants 
        SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type=%s 
        WHERE id=%s;"""
        values_tuple = (payment["Время проведения"], payment["number_of_days"],
                        payment["deadline"], participant_type, payment["participant_id"])
        # logger.info(sql_text % values_tuple)
        database.execute_dml(sql_text, values_tuple)
        logger.info("Оплата в БД отмечена")
        # Уведомление участника
        logger.info("Уведомление участника")
        notification_text = participant_notification(payment, r"[ШКОЛА ГИВИНА]. Ваша оплата принята и продлено участие в Друзьях Школы.", logger)
        mm.subject = "[ДШ] принята оплата за ДШ"
        mm.text += "Текст уведомления:\n\n\n" + notification_text
    # Окончательное состояние участника
    logger.info(f"Окончательное состояние участника\n{select_participant(payment['participant_id'], database)}")
    # Оповещение админов
    logger.info("Уведомление админов и менеджеров")
    list_ = PASSWORDS.settings['admin_emails']
    list_.extend(item for item in PASSWORDS.settings['manager_emails'] if item not in PASSWORDS.settings['admin_emails'])
    logger.info(f"list_={list_}")
    send_mail(list_, mm.subject, mm.text, logger)
    logger.info(">>>> mark_payment_into_db end")


def participant_notification(payment, subject, logger):
    logger.info(">>>> participant_notification begin")
    logger.info("Уведомление участника")
    mail_text2 = get_participant_notification_text(payment['Фамилия'], payment['Имя'], payment['login'], payment['password'])
    logger.info(f"Текст оповещения\n{mail_text2}")
    send_mail([payment["Электронная почта"]], subject, mail_text2, logger)
    logger.info(">>>> participant_notification end")
    return mail_text2


def from_list_create_sf_participants(list_, database, logger):
    """
    Создание нескольких участников ДШ по списку 
    :param logger:
    :param database:
    :param list_:
    :return: 
    """
    logger.info("Начинаю обработку списка")
    for line in list_.splitlines():
        payment = payment_creater.get_clear_payment()
        # Когда копирую из Google Sheets разделитель = Tab
        # Иванов	Иван
        # line_ = split_str(line)
        line_ = line.split(';')
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        # ['Иванов', 'Иван']
        payment["Фамилия"] = line_[0]
        payment["Имя"] = line_[1]
        try:
            if line_[2]:
                payment["Электронная почта"] = line_[2]
        except IndexError:
            pass
        try:
            if line_[3]:
                payment["telegram"] = line_[3]
        except IndexError:
            pass
        payment["Время проведения"] = datetime.now()
        payment["auto"] = False
        payment_creater.payment_normalization(payment)
        payment_creater.payment_computation(payment)
        # noinspection PyBroadException
        try:
            create_sf_participant(payment, database, logger)
        except:  # noinspection PyBroadException
            mail_text = f'Ошибка создания участника\n' + traceback.format_exc()
            logger.error(mail_text)
            send_mail(PASSWORDS.settings['admin_emails'], "ERROR CREATE PARTICIPANT", mail_text, logger)
    logger.info("Обработка списка закончена")


def create_sf_participant(payment, database, logger):
    logger.info(f">>>>sf_participant_create.create_sf_participant begin")
    # This is new participant
    # Participant must have Name, Surname, Email
    # mail_text = ""
    # subject = "НОВЫЙ УЧАСТНИК"
    mm = MailMessage("[ДШ] НОВЫЙ УЧАСТНИК", "")
    logger.info(f"Создание участника:{payment}")
    if not payment["Фамилия"]:
        logger.error("The participant must have a Surname")
        raise Exception("The participant must have a Surname")
    if not payment["Имя"]:
        logger.error("The participant must have a Name")
        raise Exception("The participant must have a Name")
    if not payment["Электронная почта"]:
        logger.warning("+" * 60)
        logger.warning("ВНИМАНИЕ: У участника нет Email!!!")
        logger.warning("+" * 60)
        # raise Exception("The participant must have a Email")
        mm.text += "\nВНИМАНИЕ: У участника нет Email!!!"
    if not payment["telegram"]:
        logger.warning("+" * 60)
        logger.warning("ВНИМАНИЕ: У участника нет Telegram!!!")
        logger.warning("+" * 60)
        # raise Exception("The participant must have a Email")
        mm.text += "\nВНИМАНИЕ: У участника нет Telegram!!!"
    # Создать участнику ДШ учётку (email) Yandex
    mm = create_sf_participant_yandex(logger, payment, mm)
    # Генерация пароля для Zoom (для всех почт пароль одинаковый)
    payment["password"] = password_for_sf()
    mm.text += f'\nPassword: {payment["password"]}'
    logger.info(f'Password: {payment["password"]}')
    # Создать участнику ДШ учётку Zoom
    mm = create_sf_participant_zoom(logger, payment, mm)
    # Создать участника ДШ в БД и отметить ему оплату
    mm = create_sf_participant_db(database, logger, payment, mm)
    # Почтовые оповещения
    # TODO Отправить Telegram участнику
    #  https://github.com/DevGivinSchool/GivinToolsPython/issues/13#issue-650152143
    logger.warning("+" * 60)
    logger.warning("TODO: Отправить уведомление участнику в Telegram.")
    logger.warning("+" * 60)
    mm.text += f"\nВНИМАНИЕ: Необходимо отправить оповещение участнику {payment['telegram']} в Telegram вручную."
    if payment["Электронная почта"]:
        # Оповещение участника
        notification_text = participant_notification(payment, r"[ШКОЛА ГИВИНА]. Поздравляем, Вы приняты в Друзья Школы", logger)
    else:
        mm.text += f"\nВНИМАНИЕ: Отправить почтовое уведомление (email) участнику"
        logger.warning("+" * 60)
        logger.warning(f"ВНИМАНИЕ: Отправить почтовое уведомление (email) участнику")
        logger.warning("+" * 60)
        notification_text = "НЕТ ТЕКСТА ОПОВЕЩЕНИЯ УЧАСТНИКА. Т.к. у участника не email"
    mm.text += "Текст уведомления:\n\n\n" + notification_text
    # send_mail(PASSWORDS.logins['admin_emails'], subject, mail_text, logger)
    # Вычитаю из списка почт менеджеров список почт админов, чтобы не было повторных писем
    logger.info("Уведомление админов и менеджеров")
    list_ = PASSWORDS.settings['admin_emails']
    list_.extend(item for item in PASSWORDS.settings['manager_emails'] if item not in PASSWORDS.settings['admin_emails'])
    logger.info(f"list_={list_}")
    send_mail(list_, mm.subject, mm.text, logger)
    logger.info(f">>>>sf_participant_create.create_sf_participant end")


def create_sf_participant_yandex(logger, payment, mm):
    # Создаём почту новому участнику в домене @givinschool.org
    logger.info("Создаём почту новому участнику в домене @givinschool.org")
    # было так
    # payment["login"] = get_login(payment["Фамилия"], payment["Имя"])
    # добавил эти 4 строчки вместо предыдущей
    payment["login"] = get_login(payment["Фамилия"], payment["Имя"]) + '@givinschool.org'
    message = f'Создать почту для\nЛогин:{payment["login"].lower()}' \
              f'\nПароль: {PASSWORDS.settings["default_ymail_password"]}' \
              f'\n{payment["Фамилия"]}' \
              f'\n{payment["Имя"]}' \
              f'\nemail: {payment["Электронная почта"]}' \
              f'\ntelegram: {payment["telegram"]} '
    print(message)
    logger.info(message)
    # region Сейчас учётка zoom создаётся из кода приложения, без получения подтверждения на email, поэтому реально почта не нужна.
    """
    try:
        result = yandex_mail.create_yandex_mail(payment["Фамилия"], payment["Имя"], payment["login"], department_id_=4)
        # print(f"Email created:{result['email']}")
        payment["login"] = result['email']
        mm.text += f'\nЯндекс почта в домене @givinschool.org успешно создана (пароль стандартный)\nЛогин для ' \
                   f'Zoom:\nLogin: {payment["login"]} '
        logger.info(f'Яндекс почта в домене @givinschool.org успешно создана (пароль стандартный)')
        logger.info(f'Логин для Zoom:')
        logger.info(f'Login: {payment["login"]}')
        # Отдел 4 = @ДРУЗЬЯ_ШКОЛЫ
    except yandex_connect.YandexConnectExceptionY as e:
        # print(e.args[0])
        if e.args[0] == 500:
            # print(f'Unhandled exception: Такая почта уже существует: {payment["login"]}')
            logger.info(f'Unhandled exception: Такая почта уже существует: {payment["login"]}')
            # Т.к. это может быть однофамилец, то ситуация требует разрешения, поэтому тут тоже падаем
            raise
        else:
            raise
    """
    # endregion
    return mm


def create_sf_participant_zoom(logger, payment, mm):
    # Создание учётки Zoom участнику
    # Для удобства создания учётки zoom записать в лог фамилию и имя
    # logger.info(f"Фамилия: {payment['Фамилия'].title()}")
    # logger.info(f"Имя: {payment['Имя'].title()}")
    logger.info("Создание учётки Zoom участнику")
    zoom_user = ZoomUS(logger)
    zoom_result = zoom_user.zoom_users_usercreate(payment["login"], payment['Имя'].title(),
                                                  payment['Фамилия'].title(), payment["password"])
    if zoom_result is not None:
        logger.error("+" * 60)
        mm.subject += " + !ZOOM ERROR"
        error_text = f"\nПрограмма не смогла создать учётку Zoom.\n" \
                     f"ВНИМАНИЕ: Необходимо создать участнику учётку в Zoom вручную." \
                     f"Создать учётку zoom участнику\nID={payment['participant_id']}\n" \
                     f"{payment['Фамилия'].title()}\n{payment['Имя'].title()}\n" \
                     f"Login: {payment['login']}\nPassword: {payment['password']}\n" \
                     f"Сведения по участнику и платежу можно посмотреть по ссылке - " \
                     f"{payment['Кассовый чек 54-ФЗ']}" \
                     f"\nERROR:\n{zoom_result}\n\n"
        mm.text += error_text
        logger.error(error_text)
        logger.error("+" * 60)
    else:
        mm.text += "\nУчётка Zoom успешно создана"
        logger.info("Учётка Zoom успешно создана")
    return mm


def create_sf_participant_db(database, logger, payment, mm):
    # Создаём нового пользователя в БД
    logger.info(f"Создаём нового пользователя в БД ({payment['fio_lang']})")
    if payment["fio_lang"] == "RUS":
        sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
        values_tuple = (payment["Фамилия"], payment["Имя"],
                        payment["Фамилия Имя"], payment["Электронная почта"],
                        payment["telegram"], 'N')
    else:
        sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type, last_name_eng, 
        first_name_eng, fio_eng) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        values_tuple = (payment["Фамилия"], payment["Имя"],
                        payment["Фамилия Имя"], payment["Электронная почта"],
                        payment["telegram"], 'N',
                        payment["Фамилия"], payment["Имя"], payment["Фамилия Имя"])
    payment["participant_id"] = database.execute_dml_id(sql_text, values_tuple)
    logger.info(select_participant(payment["participant_id"], database))
    # Отмечаем оплату в БД этому участнику
    mark_payment_into_db(payment, database, logger, participant_type='N')
    # Прикрепить участника к платежу
    if payment["auto"]:
        sql_text = """UPDATE payments SET participant_id=%s WHERE task_uuid=%s;"""
        values_tuple = (payment["participant_id"], payment["task_uuid"])
        database.execute_dml(sql_text, values_tuple)
        logger.info(select_payment(payment["task_uuid"], database))
    # Обновляем участнику логин и пароль в БД
    logger.info("Обновляем участнику логин и пароль в БД")
    sql_text = """UPDATE participants SET login=%s, password=%s WHERE id=%s;"""
    values_tuple = (payment["login"], payment["password"], payment["participant_id"])
    database.execute_dml(sql_text, values_tuple)
    # Окончательный вид участника в БД
    line = f'{select_participant(payment["participant_id"], database)}'
    mm.text += f'\nСведения об участнике успешно внесены в БД:\n{line}'
    logger.info(f'Сведения об участнике успешно внесены в БД:')
    logger.info(f'{line}')
    return mm


if __name__ == '__main__':
    import custom_logger
    import os
    from list_ import list_fio

    program_file = os.path.realpath(__file__)
    log = custom_logger.get_logger(program_file=program_file)
    # noinspection PyBroadException
    try:
        log.info("Try connect to DB")
        db = DBPostgres(dbname=PASSWORDS.settings['postgres_dbname'], user=PASSWORDS.settings['postgres_user'],
                        password=PASSWORDS.settings['postgres_password'],
                        host=PASSWORDS.settings['postgres_host'],
                        port=PASSWORDS.settings['postgres_port'], logger=log)
    except Exception:
        main_error_text = \
            f"MAIN ERROR (Postgres):\n{traceback.format_exc()}"
        print(main_error_text)
        log.error(main_error_text)
        log.error(f"Send email to: {PASSWORDS.settings['admin_emails']}")
        send_mail(PASSWORDS.settings['admin_emails'], "MAIN ERROR (Postgres)", main_error_text, log)
        log.error("Exit with error")
        sys.exit(1)
    from_list_create_sf_participants(list_fio, db, logger=log)

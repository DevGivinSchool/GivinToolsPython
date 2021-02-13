# import core.yandex_mail
# import yandex_connect
import sf.payment_creator as payment_creator
import traceback
import core.PASSWORDS as PASSWORDS
import sys
# import password_generator
from core.Class_ZoomUS import ZoomUS
from core.Class_DBPostgres import DBPostgres
from core.alert_to_mail import send_mail, get_participant_notification_text
from core.utils import get_login
from core.password_generator import password_for_sf
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
        logger.debug(f"payment до и после дополнения сведениями в mark_payment_into_db")
        logger.debug(payment)
        result = database.get_participant_by_id(payment["participant_id"])[0]
        if not payment["Фамилия"]:
            payment["Фамилия"] = result[0]
        if not payment["Имя"]:
            payment["Имя"] = result[1]
        if not payment["Фамилия Имя"]:
            payment["Фамилия Имя"] = result[2]
        if not payment["Электронная почта"]:
            payment["Электронная почта"] = result[3]
        if not payment["telegram"]:
            payment["telegram"] = result[4]
        if not payment["login"]:
            payment["login"] = result[5]
        if not payment["password"]:
            payment["password"] = result[6]
        if not payment["login1"]:
            payment["login1"] = result[7]
        # payment["level"] = result[8]
        if not payment["password1"]:
            payment["password1"] = result[9]
        logger.debug(payment)
        # [('ИВАНОВ', 'ИВАН', 'ИВАНОВ ИВАН', 'xxx@mail.ru', '@xxxx', 'ivanov_ivan@givinschool.org', '43RFji1r48')]
        logger.info("Изменение статуса участника в БД")
        sql_text = """UPDATE participants
        SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type=%s WHERE id=%s;"""
        values_tuple = (payment["Время проведения"], payment["number_of_days"],
                        payment["deadline"], participant_type, payment["participant_id"])
        database.execute_dml(sql_text, values_tuple)
        logger.info("Статус участника в БД изменён")
        # Изменение статуса в zoom
        logger.info("Активация участника в Zoom")
        zoom_user = ZoomUS(logger)
        if payment["level"] == 2:
            login_ = payment["login"]
        else:
            login_ = payment["login1"]
        logger.info(f'Активируем участника login_={login_}; level={payment["level"]}')
        zoom_result = zoom_user.zoom_users_userstatus(login_, "activate")
        if zoom_result is not None:
            if zoom_result["message"].startswith("User does not exist"):
                # Если вдруг оказалось что такого пользователя нет в zoom - пробуем его создать
                mm = create_sf_participant_zoom(logger, payment, mm)
                logger.info("Участник заново создан в Zoom")
            else:
                logger.error("+" * 60)
                mail_text = f"Процедура не смогла автоматически разблокировать участника.\n" \
                            f"Ошибка:\n" \
                            f"{zoom_result}\n" \
                            f"ID      : {payment['participant_id']}\n" \
                            f"ФИО     : {payment['Фамилия Имя']}\n" \
                            f"Login   : {login_}\n" \
                            f"Password: {payment['password']}"
                send_mail(PASSWORDS.settings['admin_emails'], "UNBLOCK PARTICIPANT ERROR", mail_text, logger,
                          attached_file=logger.handlers[0].baseFilename)
                logger.error(mail_text)
                logger.error("+" * 60)
        else:
            logger.info("Участник активирован в Zoom")
        # Уведомление участника
        logger.info("Уведомление участника")
        notification_text = participant_notification(payment,
                                                     f'[ШКОЛА ГИВИНА] Ваша учётная запись в {PASSWORDS.settings["project_name"]} разблокирована уровень {payment["level"]}.',
                                                     logger)
        mm.subject = f"[{PASSWORDS.settings['short_project_name']}] РАЗБЛОКИРОВКА УЧАСТНИКА"
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
        notification_text = participant_notification(payment,
                                                     f'[ШКОЛА ГИВИНА] Ваша оплата принята и продлено участие в онлайн-формате {PASSWORDS.settings["project_name"]} уровень {payment["level"]}.',
                                                     logger)
        mm.subject = f"[{PASSWORDS.settings['short_project_name']}] ПРИНЯТА ОПЛАТА"
        mm.text += "Текст уведомления:\n\n\n" + notification_text
    # Окончательное состояние участника
    logger.info(f"Окончательное состояние участника\n{select_participant(payment['participant_id'], database)}")
    # Оповещение админов
    logger.info("Уведомление админов и менеджеров")
    list_ = PASSWORDS.settings['admin_emails']
    list_.extend(item for item in PASSWORDS.settings['manager_emails'][payment["level"]] if item not in PASSWORDS.settings['admin_emails'])
    logger.info(f"list_={list_}")
    send_mail(list_, mm.subject, mm.text, logger)
    logger.info(">>>> mark_payment_into_db end")


def participant_notification(payment, subject, logger):
    logger.info(">>>> sf_participant_create.participant_notification begin")
    logger.info("Уведомление участника")
    mail_text2 = get_participant_notification_text(payment)
    logger.info(f"Message Subject: {subject}")
    logger.info(f"Message text:\n{mail_text2}")
    send_mail([payment["Электронная почта"]], subject, mail_text2, logger)
    logger.info(">>>> sf_participant_create.participant_notification end")
    return mail_text2


def create_sf_participants(list_, database, logger):  # noqa: C901
    """
    Создание нескольких участников КПД по списку.
    Список в формате:
    Фамилия; Имя; email; telegram
    :param logger:
    :param database:
    :param list_:
    :return:
    """
    logger.info("Начинаю обработку списка")
    line_number = 1
    for line in list_:
        print(line)
        payment = payment_creator.get_clear_payment()
        try:
            payment["Фамилия"] = line[0]
        except IndexError:
            print("Нет фамилии. Скорее всего файл list_.py пустой.")
            exit(1)
        try:
            payment["Имя"] = line[1]
        except:  # noqa: E722
            print(f"Строка №{line_number}. Нет имени, участник не создан")
            exit(1)
        try:
            if line[2]:
                payment["Электронная почта"] = line[2]
        except IndexError:
            print(f"Строка №{line_number}. Нет email, участник не создан")
            exit(1)
        try:
            if line[3]:
                payment["telegram"] = line[3]
        except IndexError:
            pass
        try:
            if line[4]:
                payment["level"] = int(line[4])
        except IndexError:
            pass
        except ValueError:
            print("ERROR: Не могу преобразовать level в целое число")
            raise
        payment["Время проведения"] = datetime.now()
        payment["auto"] = False
        payment_creator.payment_normalization(payment)
        if payment["level"] == 1:
            payment_creator.payment_computation1(payment, logger)
        else:
            payment_creator.payment_computation2(payment, logger)
        # noinspection PyBroadException
        try:
            create_sf_participant(payment, database, logger)
        except:  # noqa: E722
            mail_text = 'Ошибка создания участника\n' + traceback.format_exc()
            logger.error(mail_text)
            send_mail(PASSWORDS.settings['admin_emails'], "ERROR CREATE PARTICIPANT", mail_text, logger)
        line_number += 1
    logger.info("\n"*7)
    logger.info("Обработка списка закончена")


def create_sf_participant(payment, database, logger, special_case=False):
    logger.info(">>>>sf_participant_create.create_sf_participant begin")
    # This is new participant
    # Participant must have Name, Surname, Email
    # mail_text = ""
    # subject = "НОВЫЙ УЧАСТНИК"
    mm = MailMessage(f"[{PASSWORDS.settings['short_project_name']}] НОВЫЙ УЧАСТНИК", "")
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
    # Создать участнику КПД учётку (email) Yandex
    mm = create_sf_participant_yandex(logger, payment, mm)
    # Генерация пароля для Zoom (для всех почт пароль одинаковый)
    if payment["level"] == 2:
        if payment["password"] is None:
            payment["password"] = password_for_sf()
        mm.text += f'\nPassword: {payment["password"]}'
        logger.info(f'Password: {payment["password"]}')
    else:
        if payment["password1"] is None:
            payment["password1"] = password_for_sf()
        mm.text += f'\nPassword: {payment["password1"]}'
        logger.info(f'Password: {payment["password1"]}')
    # Создать участнику КПД учётку Zoom
    mm = create_sf_participant_zoom(logger, payment, mm)
    # Создать участника КПД в БД и отметить ему оплату
    mm = create_sf_participant_db(database, logger, payment, mm, special_case)
    # Почтовые оповещения
    # TODO Отправить Telegram участнику
    #  https://github.com/DevGivinSchool/GivinToolsPython/issues/13#issue-650152143
    logger.warning("+" * 60)
    logger.warning("TODO: Отправить уведомление участнику в Telegram.")
    logger.warning("+" * 60)
    mm.text += f"\nВНИМАНИЕ: Необходимо отправить оповещение участнику {payment['telegram']} в Telegram вручную."
    if payment["Электронная почта"]:
        # Оповещение участника
        notification_text = participant_notification(payment,
                                                     f'[ШКОЛА ГИВИНА] Поздравляем, Вы приняты в {PASSWORDS.settings["project_name"]} уровень {payment["level"]}.',
                                                     logger)
    else:
        mm.text += "\nВНИМАНИЕ: Отправить почтовое уведомление (email) участнику"
        logger.warning("+" * 60)
        logger.warning("ВНИМАНИЕ: Отправить почтовое уведомление (email) участнику")
        logger.warning("+" * 60)
        notification_text = "НЕТ ТЕКСТА ОПОВЕЩЕНИЯ УЧАСТНИКА. Т.к. у участника не email"
    mm.text += "Текст уведомления:\n\n\n" + notification_text
    # send_mail(PASSWORDS.logins['admin_emails'], subject, mail_text, logger)
    # Вычитаю из списка почт менеджеров список почт админов, чтобы не было повторных писем
    logger.info("Уведомление админов и менеджеров")
    list_ = PASSWORDS.settings['admin_emails']
    list_.extend(item for item in PASSWORDS.settings['manager_emails'][payment["level"]] if item not in PASSWORDS.settings['admin_emails'])
    logger.info(f"list_={list_}")
    send_mail(list_, mm.subject, mm.text, logger)
    logger.info(">>>>sf_participant_create.create_sf_participant end")


def create_sf_participant_yandex(logger, payment, mm):
    # Создаём почту новому участнику в домене соответствующего уровню участия
    logger.info(">>>>sf_participant_create.create_sf_participant_yandex begin")
    logger.info("Создаём почту новому участнику в домене соответствующего уровню участия")
    # было так
    # payment["login"] = get_login(payment["Фамилия"], payment["Имя"])
    # добавил эти 4 строчки вместо предыдущей
    if payment["level"] == 2:
        login_ = payment["login"] = get_login(payment["Фамилия"], payment["Имя"]) + '@givinschool.org'
    else:
        login_ = payment["login1"] = get_login(payment["Фамилия"], payment["Имя"]) + '@givinschool.com'
    message = f'Создать почту для:\n' \
              f'Логин   : {login_}\n' \
              f'Пароль  : {PASSWORDS.settings["default_ymail_password"]}\n' \
              f'Фамилия : {payment["Фамилия"]}\n' \
              f'Имя     : {payment["Имя"]}\n' \
              f'email   : {payment["Электронная почта"]}\n' \
              f'telegram: {payment["telegram"]}'
    print(message)
    logger.info(message)
    # region Сейчас учётка zoom создаётся из кода приложения, без получения подтверждения на email,
    # поэтому реально почта не нужна.
    # TODO: Сейчас два уровня, поэтому если раскоментировать,
    #  то нужно создавать учётки в @givinschool.org и в @givinschool.com
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
    logger.info(">>>>sf_participant_create.create_sf_participant_yandex end")
    return mm


def create_sf_participant_zoom(logger, payment, mm):
    # Создание учётки Zoom участнику
    # Для удобства создания учётки zoom записать в лог фамилию и имя
    # logger.info(f"Фамилия: {payment['Фамилия'].title()}")
    # logger.info(f"Имя: {payment['Имя'].title()}")
    logger.info(">>>>sf_participant_create.create_sf_participant_zoom begin")
    logger.info("Создание учётки Zoom участнику")
    zoom_user = ZoomUS(logger)
    if payment["level"] == 2:
        login_ = payment["login"]
        password_ = payment["password"]
    else:
        login_ = payment["login1"]
        password_ = payment["password1"]
    zoom_result = zoom_user.zoom_users_usercreate(login_, payment['Имя'].title(),
                                                  payment['Фамилия'].title(), password_)
    if zoom_result is not None:
        logger.error("+" * 60)
        mm.subject += " + !ZOOM ERROR"
        error_text = f"\n" \
                     f"Программа не смогла создать учётку Zoom.\n" \
                     f"ВНИМАНИЕ: Необходимо создать участнику учётку в Zoom вручную!\n" \
                     f"Создать учётку zoom участнику:\n" \
                     f"ID      : {payment['participant_id']}\n" \
                     f"Фамилия : {payment['Фамилия'].title()}\n" \
                     f"Имя     : {payment['Имя'].title()}\n" \
                     f"Login   : {login_}\n" \
                     f"Password: {payment['password']}\n" \
                     f"Сведения по участнику и платежу можно посмотреть по ссылке - {payment['Кассовый чек 54-ФЗ']}\n" \
                     f"ERROR:\n{zoom_result}\n\n"
        mm.text += error_text
        logger.error(error_text)
        logger.error("+" * 60)
    else:
        mm.text += "\nУчётка Zoom успешно создана"
        logger.info("Учётка Zoom успешно создана")
    logger.info(">>>>sf_participant_create.create_sf_participant_zoom end")
    return mm


def create_sf_participant_db(database, logger, payment, mm, special_case):
    # Создаём нового пользователя в БД если это нужно
    logger.info(">>>>sf_participant_create.create_sf_participant_db begin")
    # Участник оплатил 2 уровень но такой учётки у него еще нет. Здесь NOT чтобы обойти повторный insert
    if not special_case:
        logger.info(f"Создаём нового пользователя ({payment['fio_lang']}) в БД")
        if payment["fio_lang"] == "RUS":
            sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type, telephone, city)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
            values_tuple = (payment["Фамилия"], payment["Имя"],
                            payment["Фамилия Имя"], payment["Электронная почта"],
                            payment["telegram"], 'N', payment["phone"], payment["city"])
        else:
            sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type, last_name_eng,
            first_name_eng, fio_eng, telephone, city)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
            values_tuple = (payment["Фамилия"], payment["Имя"],
                            payment["Фамилия Имя"], payment["Электронная почта"],
                            payment["telegram"], 'N',
                            payment["Фамилия"], payment["Имя"], payment["Фамилия Имя"],
                            payment["phone"], payment["city"])
        payment["participant_id"] = database.execute_dml_id(sql_text, values_tuple)
    logger.info(select_participant(payment["participant_id"], database))
    # Отмечаем оплату в БД этому участнику
    mark_payment_into_db(payment, database, logger, participant_type='N')
    # Прикрепить участника к платежу
    if payment["auto"]:
        logger.info("Прикрепить участника к платежу")
        sql_text = """UPDATE payments SET participant_id=%s WHERE payment_id=%s;"""
        values_tuple = (payment["participant_id"], payment["ID платежа"])
        database.execute_dml(sql_text, values_tuple)
        logger.info(select_payment(payment["task_uuid"], database))
    # Обновляем участнику логин и пароль в БД
    logger.info("Обновляем участнику логин и пароль в БД и level")
    if payment["level"] == 2:
        login_ = payment["login"]
        password_ = payment["password"]
        sql_text = """UPDATE participants SET login=%s, password=%s, sf_level=%s WHERE id=%s;"""
    else:
        login_ = payment["login1"]
        password_ = payment["password1"]
        sql_text = """UPDATE participants SET login1=%s, password1=%s, sf_level=%s WHERE id=%s;"""
    values_tuple = (login_, password_, payment["level"], payment["participant_id"])
    database.execute_dml(sql_text, values_tuple)
    # Окончательный вид участника в БД
    line = f'{select_participant(payment["participant_id"], database)}'
    mm.text += f'\nСведения об участнике успешно внесены в БД:\n{line}'
    logger.info('Сведения об участнике успешно внесены в БД:')
    logger.info(f'{line}')
    logger.info(">>>>sf_participant_create.create_sf_participant_db end")
    return mm


if __name__ == '__main__':
    """ Создание участников по списку. Список в формате:
    Фамилия; Имя; email; telegram; level
    """
    import core.custom_logger as custom_logger
    import os
    import csv

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

    file = PASSWORDS.settings['list_path']
    with open(file, newline='', encoding='utf-8') as f:
        # Фамилия; Имя; email; telegram; level
        reader = csv.reader(f, delimiter=';')
        print(type(reader))
        print(reader)
        # headers = next(reader, None)
        create_sf_participants(reader, db, logger=log)

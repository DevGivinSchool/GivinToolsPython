import yandex_mail
import yandex_connect
import Parser
import traceback
import PASSWORDS
import sys
import zoom_us
import password_generator
from DBPostgres import DBPostgres
from alert_to_mail import send_mail
from utils import split_str
from utils import get_login


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
    logger.info("Отмечаем оплату в БД")
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
        login_ = result[5]
        password_ = result[6]
        # [('ИВАНОВ', 'ИВАН', 'ИВАНОВ ИВАН', 'xxx@mail.ru', '@xxxx', 'ivanov_ivan@givinschool.org', '43RFji1r48')]
        # Исправление пароля (вырезать 55 в конце)
        if password_[-2:] == "55":
            password_ = password_[:-2]
        logger.info("Разблокировка пользователя")
        sql_text = """UPDATE participants 
        SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type=%s, password=%s
        WHERE id=%s;"""
        values_tuple = (payment["Время проведения"], payment["number_of_days"],
                        payment["deadline"], participant_type, password_, payment["participant_id"])
        # Измение статуса в zoom
        zoom_result = zoom_us.zoom_users_userstatus(login_, "activate", logger=logger)
        if zoom_result is not None:
            logger.error("+" * 60)
            mail_text = f"\nПроцедура не смогла автоматически разблокировать участника. Ошибка:\n" \
                        f"{zoom_result}" \
                        f"ID={payment['participant_id']}\n{payment['Фамилия Имя']}:" \
                        f"\nLogin: {login_}\nPassword: {password_}"
            send_mail(PASSWORDS.logins['admin_emails'], "UNBLOCK PARTICIPANT ERROR", mail_text, logger)
            logger.error(mail_text)
            logger.error("+" * 60)
        else:
            logger.info("Учётка Zoom успешно активирована")

        participant_notification(payment, logger)
    else:
        sql_text = """UPDATE participants 
        SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type=%s 
        WHERE id=%s;"""
        values_tuple = (payment["Время проведения"], payment["number_of_days"],
                        payment["deadline"], participant_type, payment["participant_id"])
    # logger.info(sql_text % values_tuple)
    database.execute_dml(sql_text, values_tuple)
    # Состояние участника после отметки
    # logger.info(select_participant(payment["participant_id"], database))
    logger.info("Оплата в БД отмечена")


def participant_notification(payment, logger):
    logger.info("Уведомление участника")
    mail_text2 = f"""Здравствуйте, {payment['Фамилия Имя'].title()}!  

Поздравляем, Вы оплатили абонемент на месяц совместных занятий в онлайн-формате "Друзья Школы Гивина". 

Ваш zoom-аккаунт:
Логин: {payment['login']}
Пароль: {payment['password']}

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
    logger.info(mail_text2)
    send_mail([payment["Электронная почта"]],
              r"[ШКОЛА ГИВИНА]. Поздравляем, Вы приняты в Друзья Школы", mail_text2, logger)


def from_list_create_sf_participants(list_fio, database, logger):
    """
    Создание нескольких участников ДШ по списку 
    :param list_fio: 
    :return: 
    """
    # TODO Сделать возможность обрабатывать либо строку Ф+И либо словарь
    logger.info("Начинаю обработку списка")
    for line in list_fio.splitlines():
        payment = Parser.get_clear_payment()
        # Когда копирую из Google Sheets разделитель = Tab
        # Иванов	Иван
        line_ = split_str(line)
        # При транслитерации некоторые буквы переводятся в - ' - это нужно заменить
        # ['Иванов', 'Иван']
        payment["Фамилия"] = line_[0]
        payment["Имя"] = line_[1]
        payment["Время проведения"] = datetime.now()
        payment["auto"] = False
        Parser.payment_normalization(payment)
        Parser.payment_computation(payment)
        try:
            create_sf_participant(payment, database, logger)
        except:
            mail_text = f'Ошибка создания участника\n' + traceback.format_exc()
            logger.error(mail_text)
            send_mail(PASSWORDS.logins['admin_emails'], "ERROR CREATE PARTICIPANT", mail_text, logger)
    logger.info("Обработка списка закончена")


def create_sf_participant(payment, database, logger):
    # This is new participant
    # Participant must have Name, Surname, Email
    mail_text = ""
    subject = "НОВЫЙ УЧАСТНИК"
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
        mail_text += "\nВНИМАНИЕ: У участника нет Email!!!"
    if not payment["telegram"]:
        logger.warning("+" * 60)
        logger.warning("ВНИМАНИЕ: У участника нет Telegram!!!")
        logger.warning("+" * 60)
        # raise Exception("The participant must have a Email")
        mail_text += "\nВНИМАНИЕ: У участника нет Telegram!!!"

    # Создаём нового пользователя в БД
    logger.info(f"Создаём нового пользователя в БД ({payment['fio_lang']})")
    if payment["fio_lang"] == "RUS":
        sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
        values_tuple = (payment["Фамилия"], payment["Имя"],
                        payment["Фамилия Имя"], payment["Электронная почта"],
                        payment["telegram"], 'N')
    else:
        sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type, last_name_eng, first_name_eng, fio_eng) 
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

    # Создаём почту новому участнику в домене @givinschool.org
    logger.info("Создаём почту новому участнику в домене @givinschool.org")
    payment["login"] = get_login(payment["Фамилия"], payment["Имя"])
    try:
        result = yandex_mail.create_yandex_mail(payment["Фамилия"], payment["Имя"], payment["login"], department_id_=4)
        # print(f"Email created:{result['email']}")
        payment["login"] = result['email']
        mail_text += f'\nСоздана почта в домене @givinschool.org\nLogin: {payment["login"]}'
        logger.info(f'Создана почта в домене @givinschool.org')
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
    # Для удобства создания учётки zoom записать в лог фамилию и имя
    # logger.info(f"Фамилия: {payment['Фамилия'].title()}")
    # logger.info(f"Имя: {payment['Имя'].title()}")
    # Генерация пароля для Zoom (для всех почт пароль одинаковый)
    payment["password"] = password_generator.random_password(strong=True, zoom=True)
    mail_text += f'\nPassword: {payment["password"]}'
    logger.info(f'Password: {payment["password"]}')
    logger.info("Обновляем участнику логин и пароль в БД")
    sql_text = """UPDATE participants SET login=%s, password=%s WHERE id=%s;"""
    values_tuple = (payment["login"], payment["password"], payment["participant_id"])
    database.execute_dml(sql_text, values_tuple)
    # Окончательный вид участника в БД
    line = f'{select_participant(payment["participant_id"], database)}'
    mail_text += f'\nУчастник в БД:\n{line}'
    logger.info(f'Участник в БД:')
    logger.info(f'{line}')

    # Создание учётки Zoom участнику
    logger.info("Создание учётки Zoom участнику")
    zoom_result = zoom_us.zoom_users_usercreate(payment["login"], payment['Имя'].title(),
                                                payment['Фамилия'].title(), payment["password"], logger=logger)
    if zoom_result is not None:
        logger.error("+" * 60)
        subject += " + !ZOOM ERROR"
        error_text = f"\nПрограмма не смогла создать учётку Zoom.\n" \
                     f"ВНИМАНИЕ: Необходимо создать участнику учётку в Zoom вручную." \
                     f"Создать учётку zoom участнику\nID={payment['participant_id']}\n" \
                     f"{payment['Фамилия'].title()}\n{payment['Имя'].title()}\n" \
                     f"Login: {payment['login']}\nPassword: {payment['password']}\n" \
                     f"Сведения по участнику и платежу можно посмотреть по ссылке - " \
                     f"{payment['Кассовый чек 54-ФЗ']}" \
                     f"\nERROR:\n{zoom_result}\n\n"
        mail_text += error_text
        logger.error(error_text)
        logger.error("+" * 60)
    else:
        mail_text += "\nУчётка Zoom успешно создана"
        logger.info("Учётка Zoom успешно создана")

    # Почтовые оповещения
    # TODO Отправить Telegram участнику
    logger.warning("+" * 60)
    logger.warning("TODO: Отправить уведомление участнику в Telegram.")
    logger.warning("+" * 60)
    mail_text += f"\nВНИМАНИЕ: Отправить Telegram участнику {payment['telegram']}"
    if payment["Электронная почта"]:
        participant_notification(payment, logger)
    else:
        mail_text += f"\nВНИМАНИЕ: Отправить почтовое уведомление (email) участнику"
        logger.warning("+" * 60)
        logger.warning(f"ВНИМАНИЕ: Отправить почтовое уведомление (email) участнику")
        logger.warning("+" * 60)
    send_mail(PASSWORDS.logins['admin_emails'], subject, mail_text, logger)
    # Вычитаю из списка почт менеджеров список почт админов, чтобы не было повторных писем
    list_ = [item for item in PASSWORDS.logins['manager_emails'] if item not in PASSWORDS.logins['admin_emails']]
    send_mail(list_, subject, mail_text, logger)


if __name__ == '__main__':
    import logging
    from list import list_fio
    from datetime import datetime
    from Log import Log
    from log_config import log_dir, log_level

    now = datetime.now().strftime("%Y%m%d%H%M")
    logger = Log.setup_logger('__main__', log_dir, f'gtp_create_login_{now}.log', logging.DEBUG)
    try:
        logger.info("Try connect to DB")
        database = DBPostgres(dbname=PASSWORDS.logins['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                              password=PASSWORDS.logins['postgres_password'],
                              host=PASSWORDS.logins['postgres_host'],
                              port=PASSWORDS.logins['postgres_port'], logger=logger)
    except Exception:
        # TODO Вынести процедуру опопвещения MAIN ERROR в отдельную процедуру
        error_text = \
            f"MAIN ERROR (Postgres):\n{traceback.format_exc()}"
        print(error_text)
        logger.error(error_text)
        logger.error(f"Send email to: {PASSWORDS.logins['admin_emails']}")
        send_mail(PASSWORDS.logins['admin_emails'], "MAIN ERROR (Postgres)", error_text, logger)
        logger.error("Exit with error")
        sys.exit(1)
    from_list_create_sf_participants(list_fio, database, logger=logger)

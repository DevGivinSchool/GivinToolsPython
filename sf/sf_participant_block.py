import traceback
import core.PASSWORDS as PASSWORDS
from core.Class_ZoomUS import ZoomUS
from core.alert_to_mail import send_mail
from core.Class_DBPostgres import DBPostgres
from core.utils import is_eng, is_rus


def participants_block(list_participants, logger2):
    # Подключение к БД
    postgres = DBPostgres(dbname=PASSWORDS.settings['postgres_dbname'], user=PASSWORDS.settings['postgres_user'],
                          password=PASSWORDS.settings['postgres_password'], host=PASSWORDS.settings['postgres_host'],
                          port=PASSWORDS.settings['postgres_port'], logger=logger2)
    for p in list_participants.splitlines():
        block_one_participant(p, postgres, logger2)
    postgres.disconnect()


def block_one_participant(p, postgres, logger):  # noqa: C901
    print(f"Попытка блокировки участника |{p}|")
    logger.info(f"Попытка блокировки участника |{p}|")
    # Проверяем что p это ID
    sql_instr = ""
    participant = None
    if isinstance(p, int):
        sql_instr = "id"
        print(f"Ищем участника по ID - {p}")
        logger.info(f"Ищем участника по ID - {p}")
        participant = postgres.find_participant_by('id', p)
    else:
        p = p.strip()
        if p[0] == '@':
            # Ищем участника по Telegram
            sql_instr = "telegram"
            p = p.lower()
            print(f"Ищем участника по Telegram - {p}")
            logger.info(f"Ищем участника по Telegram - {p}")
            participant = postgres.find_participant_by('telegram', p)
        elif '@' in p:
            # Ищем участника по email
            sql_instr = "email"
            p = p.lower()
            print(f"Ищем участника по email - {p}")
            logger.info(f"Ищем участника по email - {p}")
            participant = postgres.find_participant_by('email', p)
        elif is_rus(p):
            # Ищем участника по fio
            sql_instr = "fio"
            p = p.upper()
            print(f"Ищем участника по fio - {p}")
            logger.info(f"Ищем участника по fio - {p}")
            participant = postgres.find_participant_by('fio', p)
        elif is_eng(p):
            # Ищем участника по fio_eng
            sql_instr = "fio_eng"
            p = p.upper()
            print(f"Ищем участника по fio_eng - {p}")
            logger.info(f"Ищем участника по fio_eng - {p}")
            participant = postgres.find_participant_by('fio_eng', p)
    if participant is None:
        print(f"******* ВНИМАНИЕ: По значению {p} ничего не нашлось")
        logger.warning(f"******* ВНИМАНИЕ: По значению {p} ничего не нашлось")
        print("-" * 45)
    else:
        if participant['type'] == 'N' or participant['type'] == 'P':
            # Блокируем пользователя
            # sql_text = f"UPDATE participants SET type='B', password=password||'55' where {sql_instr}=%s RETURNING id;"
            sql_text = f"UPDATE participants SET type='B' where {sql_instr}=%s RETURNING id;"
            values_tuple = (p,)
            id_ = postgres.execute_dml_id(sql_text, values_tuple)
            if id_ is None:
                print(f"******* ВНИМАНИЕ: UPDATE для {p} не отработал")
                logger.error(f"******* ВНИМАНИЕ: UPDATE для {p} не отработал")
            else:
                print(f"Блокировка участника ID={id_}")
                logger.info(f"Блокировка участника ID={id_}")
                # Состояние участник
                sql_text = 'SELECT id, fio, login, password, type, login1, sf_level, password1 FROM participants where id=%s;'
                # [(1420, 'ВОЛЬНЫХ НАТАЛЬЯ', 'volnyh_natalja@givinschool.org', 'password', 'B')]
                values_tuple = (id_,)
                participant = postgres.execute_select(sql_text, values_tuple)[0]
                print(participant)
                logger.debug(f"participant={participant}")
                # Измение статуса в zoom (блокировка участника)
                print("Блокировка участника в Zoom")
                logger.info("Блокировка участника в Zoom")
                zoom_user = ZoomUS(logger)
                if participant[6] == 1:  # level
                    login_ = participant[5]  # login1
                else:
                    login_ = participant[2]  # login
                zoom_result = zoom_user.zoom_users_userstatus(login_, "deactivate")
                print(zoom_result)
                logger.debug(f"zoom_result={zoom_result}")
                if zoom_result is not None:
                    logger.error("+" * 60)
                    mail_text = f"\nПроцедура не смогла автоматически заблокировать участника. Ошибка:\n" \
                                f"{zoom_result}\n" \
                                f"ID: {participant[0]}\nFIO: {participant[1]}\n" \
                                f"Level: {participant[6]}\n" \
                                f"Login: {login_}\nPassword: {participant[3]}"
                    send_mail(PASSWORDS.settings['admin_emails'], "BLOCK PARTICIPANT ERROR", mail_text, logger)
                    print(mail_text)
                    logger.error(mail_text)
                    logger.error("+" * 60)
                else:
                    print("Учётка Zoom успешно заблокирована")
                    logger.info("Учётка Zoom успешно заблокирована")
        elif participant['type'] == 'B':
            print("ЭТОТ УЧАСТНИК УЖЕ ЗАБЛОКИРОВАН")
            logger.info("ЭТОТ УЧАСТНИК УЖЕ ЗАБЛОКИРОВАН")
        else:
            print(f"Неизвестный тип участника type={participant['type']}")
            logger.warning(f"Неизвестный тип участника type={participant['type']}")
        print("-" * 45)
        logger.info("-" * 45)


if __name__ == '__main__':
    import core.custom_logger as custom_logger
    import os
    import csv
    # from list_ import list_fio

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
        exit(1)

    file = PASSWORDS.settings['list_path']
    with open(file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        # headers = next(reader, None)
        for row in reader:
            print(row[0])
            print(type(row[0]))
            block_one_participant(row[0], db, log)

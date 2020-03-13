import PASSWORDS
import zoom_us
from alert_to_mail import send_mail
from DBPostgres import DBPostgres
from utils import is_eng
from utils import is_rus


def participant_block(list_participants, logger):
    # Подключение к БД
    postgres = DBPostgres(dbname=PASSWORDS.logins['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                          password=PASSWORDS.logins['postgres_password'], host=PASSWORDS.logins['postgres_host'],
                          port=PASSWORDS.logins['postgres_port'])
    for p in list_participants.splitlines():
        print(f"Попытка блокировки участника |{p}|")
        logger.info(f"Попытка блокировки участника |{p}|")
        p = p.strip()
        participant_id = None
        if p[0] == '@':
            # Ищем участника по Telegram
            sql_instr = "telegram"
            p = p.lower()
            print(f"Ищем участника по Telegram - {p}")
            logger.info(f"Ищем участника по Telegram - {p}")
            participant_id, p_type = postgres.find_participant_by('telegram', p)
        elif '@' in p:
            # Ищем участника по email
            sql_instr = "email"
            p = p.lower()
            print(f"Ищем участника по email - {p}")
            logger.info(f"Ищем участника по email - {p}")
            participant_id, p_type = postgres.find_participant_by('email', p)
        elif is_rus(p):
            # Ищем участника по fio
            sql_instr = "fio"
            p = p.upper()
            print(f"Ищем участника по fio - {p}")
            logger.info(f"Ищем участника по fio - {p}")
            participant_id, p_type = postgres.find_participant_by('fio', p)
        elif is_eng(p):
            # Ищем участника по fio_eng
            sql_instr = "fio_eng"
            p = p.upper()
            print(f"Ищем участника по fio_eng - {p}")
            logger.info(f"Ищем участника по fio_eng - {p}")
            participant_id, p_type = postgres.find_participant_by('fio_eng', p)
        if participant_id is None:
            print(f"******* ВНИМАНИЕ: По значению {p} ничего не нашлось")
            logger.warning(f"******* ВНИМАНИЕ: По значению {p} ничего не нашлось")
            print("-" * 45)
            continue
        if p_type == 'N' or p_type == 'P':
            # Блокируем пользователя
            # sql_text = f"UPDATE participants SET type='B', password=password||'55' where {sql_instr}=%s RETURNING id;"
            sql_text = f"UPDATE participants SET type='B' where {sql_instr}=%s RETURNING id;"
            values_tuple = (p,)
            id_ = postgres.execute_dml_id(sql_text, values_tuple)
            if id_ is None:
                print(f"******* ВНИМАНИЕ: UPDATE для {p} не отработал")
                logger.error(f"******* ВНИМАНИЕ: UPDATE для {p} не отработал")
            else:
                print(f"Заблокирован участник ID={id_}")
                logger.info(f"Заблокирован участник ID={id_}")
                # Состояние участник
                sql_text = 'SELECT id, fio, login, password, type FROM participants where id=%s;'
                # [(1420, 'ВОЛЬНЫХ НАТАЛЬЯ', 'volnyh_natalja@givinschool.org', 'Z7#A5Ycddq55', 'B')]
                values_tuple = (id_,)
                participant = postgres.execute_select(sql_text, values_tuple)[0]
                print(participant)
                logger.debug(f"participant={participant}")
                # Измение статуса в zoom (блокировка участника)
                zoom_result = zoom_us.zoom_users_userstatus(participant[2], "deactivate", logger=logger)
                print(zoom_result)
                logger.debug(f"zoom_result={zoom_result}")
                if zoom_result is not None:
                    logger.error("+" * 60)
                    mail_text = f"\nПроцедура не смогла автоматически заблокировать участника. Ошибка:\n" \
                                f"{zoom_result}" \
                                f"ID={participant[0]}\n{participant[1]}:" \
                                f"\nLogin: {participant[2]}\nPassword: {participant[3]}"
                    send_mail(PASSWORDS.logins['admin_emails'], "BLOCK PARTICIPANT ERROR", mail_text, logger)
                    print(mail_text)
                    logger.error(mail_text)
                    logger.error("+" * 60)
                else:
                    print("Учётка Zoom успешно заблокирована")
                    logger.info("Учётка Zoom успешно заблокирована")
        elif p_type == 'B':
            print("ЭТОТ УЧАСТНИК УЖЕ ЗАБЛОКИРОВАН")
            logger.info("ЭТОТ УЧАСТНИК УЖЕ ЗАБЛОКИРОВАН")
        else:
            print(f"Неизвестный тип участника type={p_type}")
            logger.info(f"Неизвестный тип участника type={p_type}")
        print("-" * 45)
        logger.info("-" * 45)
    postgres.disconnect()


if __name__ == '__main__':
    from Log import Log
    from log_config import log_dir, log_level
    from datetime import datetime

    list_participants = """
"""

    now = datetime.now().strftime("%Y%m%d%H%M")
    logger = Log.setup_logger('__main__', log_dir, f'gtp_block_participant_{now}.log',
                              log_level)

    participant_block(list_participants, logger)

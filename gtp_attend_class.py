"""
Отмечать присутствие на занятиях и получать итоговую таблицу
"""
"""!!! можно отмечать присутствие из программы циклом, а можно одним sql запросом, но нужно это делать циклом, 
потому что есть соотвествия написания имени в zoom и членом команды отраженное в таблице zoom_join_zoom_and_members, 
поэтому каждый раз могут появляться иные соответсвия и такие люди не будет отмечены и это никак не обнаружиться, 
поэтому нужно идти циклом, отмечать присутствие и в конце выводить список выявленных новых соответствий, 
их нужно заносить в таблицу вручную, ПОТОМУ ЧТО ТОЛЬКО ЧЕЛОВЕК СМОЖЕТ УСТАНОВИТЬ РЕАЛЬНОЕ СООТВЕТСВИЕ (люди иногда 
так называют себя что там сам чёрт ногу сломит). 

select 
--*
tm.id, tm.last_name, tm.first_name, sum(conference_duration) as conference_duration 
from team_members tm
LEFT JOIN (select * from (select zoom_name, zoom_email, sum(conference_duration) as conference_duration
from zoom_conference_participants
WHERE conference_id=305 
group by zoom_name, zoom_email) zcp
LEFT JOIN zoom_join_zoom_and_members jm
            ON zcp.zoom_name = jm.zoom_name) tab1
			ON tm.id = tab1.member_id
where tm.id<>1
group by tm.id, tm.last_name, tm.first_name
order by tm.last_name
"""
import csv
import traceback
import PASSWORDS
import sys
import utils
from Log import Log
from log_config import log_dir, log_level
from datetime import datetime
from DBPostgres import DBPostgres


def convert_zoom_datetime(text):
    """
    Преобразование даты из формата zoom (04/10/2020 08:48:54 PM) в datetime
    :param text: Строка даты формата zoom
    :return: Тип datetime
    """
    return datetime.strptime(text, '%m/%d/%Y %I:%M:%S %p')


def get_header(file, logger):
    """
    Парсинг заголовка отчёта (первые два строки). Сведения о конференции.
    :param file: Файл отчёта
    :param logger: логгер
    :return: Кортеж сведений о конференции
    """
    logger.info("Получение заголовка отчёта")
    with open(file, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader, None)
        header = next(reader, None)
        header[0] = int(header[0])
        header[2] = convert_zoom_datetime(header[2])
        header[3] = convert_zoom_datetime(header[3])
        header[5] = int(header[5])
        header[6] = int(header[6])
        header = header[0:7]
        header = tuple(header)
    logger.info("Заголовок:")
    logger.info(header)
    return header


def get_participants_list(file, conference_id, logger):
    """
    Получение списка участников конференции из файла отчёта.
    :param conference_id: ID конференции
    :param file: Файл отчёта
    :param logger: логгер
    :return: Список кортежей участников конференции
    """
    logger.info("Получение списка участников")
    participants_list = []
    with open(file, "r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        # Цикл для пропуска всех заголовков
        logger.info("Пропуск всех заголовков")
        for _ in reader:
            headers = next(reader, None)
            # print(headers)
            if not headers[0] == "Имя (настоящее имя)":
                continue
            else:
                break
        logger.info("Преобразование списка участников")
        for row in reader:
            # print(row)
            logger.info(row)
            # ['Павел Павлов', 'xxxx@gmail.com', '04/10/2020 07:21:08 PM', '04/10/2020 08:48:53 PM', '88']
            row[1] = row[1].strip().lower()
            row[2] = convert_zoom_datetime(row[2])
            row[3] = convert_zoom_datetime(row[3])
            row[4] = int(row[4])
            row.append(conference_id)
            # ['Павел Павлов', 'xxxx@gmail.com', '04/10/2020 07:21:08 PM', '04/10/2020 08:48:53 PM', 88, 305]
            participants_list.append(tuple(row))
        logger.info("Список участников:")
        logger.info(participants_list)
    return participants_list


def mark_attendance(file, db, col_name, logger):
    """
    Читает отчёт zoom, парсит его и заносит все полученные данные в БД
    :param file: Файл отчёта
    :param logger: логгер
    :param db: Экземляр DBPostgres для работы с БД
    """
    # Парсинг заголовка отчёта
    header = None
    conference_id = None
    participants_list = None
    try:
        header = get_header(file, logger)
    except:
        error_fixing(f"ERROR: Can't get header:\n{traceback.format_exc()}", logger)
    # На основе данных парсинга заголовка отчёта создание конференции
    try:
        logger.info("Создание конференции")
        sql_text = """INSERT INTO public.zoom_conferences(zoom_conference_id, conference_name, time_begin, time_end, 
        zoom_login, conference_duration, number_conference_participants) VALUES (%s, %s, %s, %s, %s, %s, 
        %s) RETURNING id; """
        conference_id = db.execute_dml_id(sql_text, header)
        logger.info(f"Создана конференция id={conference_id}")
    except:
        error_fixing(f"ERROR: Can't create conference:\n{traceback.format_exc()}", logger)
    # Парсинг и получение списка участников
    try:
        participants_list = get_participants_list(file, conference_id, logger)
    except:
        error_fixing(f"ERROR: Can't get participants list:\n{traceback.format_exc()}", logger)
    logger.info(f"Вставка списка участников в базу данных")
    list_p = []  # Список участников для которых не нашлось соответсвия и их нужно вставить вручную
    participants_count = len(participants_list)
    print(f"Всего {participants_count} участников")
    ii = 0
    for p in participants_list:
        logger.info(f"Создать участника:{p}")
        try:
            sql_text = """INSERT INTO public.zoom_conference_participants(zoom_name, zoom_email, time_begin, 
            time_end, conference_duration, conference_id) VALUES (%s, %s, %s, %s, %s, %s); """
            db.execute_dml(sql_text, p)
            # Выяснить какие члены команды связаны с этим участником
            pid = db.find_zoom_participant_by(p)
            if pid is None:
                logger.warning(f"Соответствие не нашлось")
                list_p.append(p)
            else:
                # Отметить присутствие в таблице
                row_count = db.mark_zoom_attendance(col_name, pid, p, logger)
                if row_count == 0:
                    logger.warning(f"Ничего не отметилось")
        except:
            error_text = f"ERROR: Create participant:\n{traceback.format_exc()}"
            print(error_text)
            logger.error(error_text)
        ii += 1
        print(f"обработано {ii} участников из {participants_count}")
    logger.info("=" * 80)
    logger.info("=" * 80)
    if len(list_p) > 0:
        print("ВНИМАНИЕ! Есть несоответсвия")
        logger.info("Списко участников для которых не нашлось соотвествия с членами команды")
        for i in list_p:
            print(i)
            logger.info(i)
        buffer = "\n"
        for i in list_p:
            buffer += f"INSERT INTO public.zoom_join_zoom_and_members(zoom_name, zoom_email, zoom_name_norm, " \
                      f"member_id) VALUES ('{i[0]}', '{i[1]}', '{utils.str_normalization1(i[0])}', 7777);\n"
        logger.info(buffer)


def error_fixing(error_text, logger):
    print(error_text)
    logger.error(error_text)
    # logger.error(f"Send email to: {PASSWORDS.logins['admin_emails']}")
    # send_mail(PASSWORDS.logins['admin_emails'], "MAIN ERROR (Postgres)", error_text, logger)
    logger.error("Exit with error")
    sys.exit(1)


if __name__ == '__main__':
    file_path = r"c:\!SAVE\Посещение\1404-1.csv"
    col_name = "D1404_1"

    now = datetime.now().strftime("%Y%m%d%H%M")
    logger = Log.setup_logger('__main__', log_dir, f'gtp_attend_class_{now}.log',
                              log_level)
    logger.info(f"Обрабатываю файл отчёта:{file_path}")
    logger.info("Try connect to DB")
    db = None
    try:
        db = DBPostgres(dbname=PASSWORDS.logins['postgres_dbname'],
                        user=PASSWORDS.logins['postgres_user'],
                        password=PASSWORDS.logins['postgres_password'],
                        host=PASSWORDS.logins['postgres_host'],
                        port=PASSWORDS.logins['postgres_port'],
                        logger=logger)
    except:
        error_fixing(f"ERROR: Connect to Postgres:\n{traceback.format_exc()}", logger)
    logger.info("Connect to DB is OK")
    mark_attendance(file_path, db, col_name, logger)
    logger.info(f"Обработка отчёта закончена.")

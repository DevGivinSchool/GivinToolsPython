import datetime
import core.utils as utils
import psycopg2
import sf.payment_creator as payment_creator
import core.PASSWORDS as PASSWORDS


class DBPostgres:

    def __init__(self, dbname, host, logger, port='5432', user='postgres',
                 password='postgres'):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password,
                                     host=self.host, port=self.port)
        self.logger = logger

    def execute_select(self, sql_text, values_tuple):
        """Execute selects
           :param values_tuple:
           :param sql_text: Query text.
           :return: List of tuples = List of strings"""
        cursor = self.conn.cursor()
        if PASSWORDS.DEBUG:
            self.logger.debug(cursor.mogrify(sql_text, values_tuple))
            print(cursor.mogrify(sql_text, values_tuple))
        cursor.execute(sql_text, values_tuple)
        records = cursor.fetchall()
        # print(cursor.rowcount)
        cursor.close()
        return records

    def execute_dml(self, sql_text, values_tuple):
        """Execute DML operations
                   :param values_tuple: Values
                   :param sql_text: Query text.
                   :return: Rows count"""
        cursor = self.conn.cursor()
        if PASSWORDS.DEBUG:
            self.logger.debug(cursor.mogrify(sql_text, values_tuple))
            print(cursor.mogrify(sql_text, values_tuple))
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        # print(cursor.rowcount)
        cursor.close()
        return cursor.rowcount

    def execute_dml_id(self, sql_text, values_tuple):
        """Execute DML operations
                   :param values_tuple:
                   :param sql_text: Query text.
                   :return: ID"""
        cursor = self.conn.cursor()
        if PASSWORDS.DEBUG:
            self.logger.debug(cursor.mogrify(sql_text, values_tuple))
            print(cursor.mogrify(sql_text, values_tuple))
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        # print(cursor.rowcount)
        if cursor.rowcount == 0:
            id_ = None
        else:
            id_ = cursor.fetchone()[0]
        cursor.close()
        return id_

    ###########################################################################

    def get_participant_by_id(self, value):
        """
        Возвращает основные сведения участника по ID
        :param value: ID
        :return:
        """
        sql_text = r"select last_name, first_name, fio, email, telegram, login, password, login1, sf_level, password1 from participants where id=%s;"
        values_tuple = (value,)
        return self.execute_select(sql_text, values_tuple)

    def create_task(self, session_id, task):
        """
        Create new task. If the task already exist, then increase attempt count.
        :param session_id:
        :param task:
        :return: True - It is new task; False - It is reprocessing task
        """
        self.logger.info(">>>>Class_DBPostgres.create_task begin")
        cursor = None
        try:
            cursor = self.conn.cursor()
            # Решил не писать в tasks поля body, т.к. база пухнет, а эту информацию можно и в почте посмотреть.
            sql_text = """INSERT INTO tasks
            (time_begin, task_from, task_subject, task_uuid, session_id)
            VALUES (NOW(), %s, %s, %s, %s) RETURNING task_uuid;"""
            values_tuple = (task.ffrom, task.subject, task.uuid, session_id)
            cursor.execute(sql_text, values_tuple)
        except psycopg2.errors.UniqueViolation as e:
            """ If that row already exist, than update attempts"""
            self.conn.rollback()
            cursor.close()
            self.logger.error(f"psycopg2.Error::\n{e.pgerror}\n{e.diag.message_detail}")
            try:
                cursor = self.conn.cursor()
                sql_text = """UPDATE tasks set number_of_attempts = number_of_attempts + 1 where task_uuid=%s;"""
                values_tuple = (task.uuid,)
                cursor.execute(sql_text, values_tuple)
                self.conn.commit()
                return False
            except Exception as e:
                self.logger.error(f"Exception::\n{e}")
                raise
        try:
            sql_text = """INSERT INTO sessions_tasks(task_uuid, session_id) VALUES (%s, %s);"""
            values_tuple = (task.uuid, session_id)
            cursor.execute(sql_text, values_tuple)
        except Exception as e:
            self.logger.error(f"Exception::\n{e}")
            raise
        self.conn.commit()
        # task_uuid_ = cursor.fetchone()[0]
        cursor.close()
        self.logger.info(">>>>Class_DBPostgres.create_task end")
        return True

    def task_error(self, error_text, task_uuid):
        """
        Log Task error
        :param task_uuid:
        :param error_text:
        :return:
        """
        cursor = self.conn.cursor()
        sql_text = """UPDATE tasks SET task_error=%s WHERE task_uuid=%s;"""
        values_tuple = (error_text, task_uuid)
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        cursor.close()

    def session_end(self, session_id):
        cursor = self.conn.cursor()
        sql_text = """update sessions set time_end=NOW() where id=%s;"""
        values_tuple = (session_id,)
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        count = cursor.rowcount
        cursor.close()
        return count

    def create_payment_in_db(self, task):
        """
        Создание платежа. К платежу сразу привязывается плательщик, если находится соответствие по почте или ФИО
        :param task:
        :return:
        """
        self.logger.info(">>>>Class_DBPostgres.create_payment_in_db begin")
        # Ищем участника сначала по email
        self.logger.info("Поиск участника по различным критериям (если это новенький, то ничего не найдётся")
        self.logger.info(f"Ищем участника сначала по email - {task.payment['Электронная почта']}")
        participant = self.find_participant_by('email', task.payment["Электронная почта"])
        if participant['id'] is None:
            # Ищем по fio в зависимости от языка RUS\ENG
            self.logger.info(f"Ищем участника по fio - {task.payment['Фамилия Имя']}")
            if task.payment["fio_lang"] == "RUS":
                self.logger.info("fio_lang = RUS")
                participant = self.find_participant_by('fio', task.payment["Фамилия Имя"])
            else:  # Иначе ищем по ENG потому что после парсера никаких других языков быть не может
                self.logger.info("fio_lang = ENG")
                participant = self.find_participant_by('fio_eng', task.payment["Фамилия Имя"])
            if participant['id'] is None and task.payment["Платежная система"] == 1:
                self.logger.info("Ничего не найдено, поэтому пробуем парсить страницу заказа")
                # Если это Getcourse и ничего по ФИО и почте (которой могло и не быть) не нашлось,
                # тогда парсим страницу GetCourse, если есть ссылка на неё,
                # и пытаемся еще раз поискать по почте и телеграм
                if task.payment["Кассовый чек 54-ФЗ"] and not task.payment["Кассовый чек 54-ФЗ"].startswith("http://order_number"):
                    payment_creator.parse_getcourse_page(task.payment["Кассовый чек 54-ФЗ"], task.payment, self.logger)
                    self.logger.info(f"Ищем участника повторно по email - {task.payment['Электронная почта']}")
                    participant = self.find_participant_by('email', task.payment["Электронная почта"])
                    if participant['id'] is None:
                        self.logger.info(f"Ищем участника по Telegram - {task.payment['telegram']}")
                        participant = self.find_participant_by('telegram', task.payment["telegram"])
        self.logger.info("Поиск участника окончен")
        self.logger.info("Дополнение платежа созданного после парсинга письма сведениями из БД из найденного участника")
        # Дополнение платежа созданного после парсинга письма сведениями из БД из найденного участника.
        if participant['id'] is not None:  # Это старенький участник, для него можно получить сведения из БД
            self.logger.info("Участник найден - это не новичок")
            if not task.payment["participant_id"]:
                task.payment["participant_id"] = participant['id']
            if not task.payment["participant_type"]:
                task.payment["participant_type"] = participant['type']
            if not task.payment["Электронная почта"]:
                task.payment["Электронная почта"] = participant['email']
            if not task.payment["telegram"]:
                task.payment["telegram"] = participant['telegram']
            if not task.payment["login"]:
                task.payment["login"] = participant['login']
            if not task.payment["password"]:
                task.payment["password"] = participant['password']
            if not task.payment["login1"]:
                task.payment["login1"] = participant['login1']
            # task.payment["level"] = participant['sf_level']
            if not task.payment["password1"]:
                task.payment["password1"] = participant['password1']
            # issues 2. Если срок платежа не закончился то нужно прибавлять эти дни.
            # Для новеньких это не нужно.
            # Срок окончания оплаченного периода может быть как deadline, так и until_date.
            if participant['until_date'] is not None:
                end_date = participant['until_date']
                self.logger.debug(f"end_date=until_date=|{type(end_date)}|{end_date}|")
            else:
                end_date = participant['deadline']
                self.logger.debug(f"end_date=deadline=|{type(end_date)}|{end_date}|")
            if task.payment["Время проведения"].date() < end_date:
                days_ = (end_date - task.payment["Время проведения"].date()).days
                self.logger.debug(
                    f"task.payment[deadline]1=|{type(task.payment['deadline'])}|{task.payment['deadline']}|")
                task.payment["deadline"] = task.payment["deadline"] + datetime.timedelta(days=days_)
                self.logger.debug(
                    f"task.payment[deadline]2=|{type(task.payment['deadline'])}|{task.payment['deadline']}|")
                task.payment["number_of_days"] = task.payment["number_of_days"] + days_
                self.logger.info(f"Добавлено {days_} дней")
                self.logger.debug(f"task.payment[number_of_days]={task.payment['number_of_days']}")
        self.logger.info(f'payment\n{task.payment}')
        cursor = self.conn.cursor()
        sql_text = """INSERT INTO payments(task_uuid, name_of_service, payment_id, amount, participant_id,
        sales_slip, card_number, card_type, payment_purpose, last_name, first_name, fio, email, payment_system,
        log_file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING task_uuid;"""
        values_tuple = (task.uuid, task.payment["Наименование услуги"], task.payment["ID платежа"],
                        task.payment["Оплаченная сумма"], task.payment["participant_id"],
                        task.payment["Кассовый чек 54-ФЗ"],
                        task.payment["Номер карты"], task.payment["Тип карты"], 1, task.payment["Фамилия"],
                        task.payment["Имя"], task.payment["Фамилия Имя"], task.payment["Электронная почта"],
                        task.payment["Платежная система"], self.logger.handlers[0].baseFilename)
        # print(values_tuple)
        self.logger.debug(f'values_tuple={values_tuple}')
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        id_ = cursor.fetchone()[0]
        cursor.close()
        task.payment["task_uuid"] = id_
        self.logger.info(
            f"Payment {task.payment['task_uuid']} for participant {task.payment['participant_id']}|"
            f"{task.payment['participant_type']} created")
        self.logger.info(f'Платёж после всех дополнений:\n{task.payment}')
        self.logger.info(">>>>Class_DBPostgres.create_payment_in_db end")

    def create_column(self, col_name):
        sql_text = "SELECT column_name FROM information_schema.columns WHERE table_name='zoom_table' and column_name" \
                   "=%s; "
        values_tuple = (col_name,)
        self.logger.info(f"SELECT column_name FROM information_schema.columns WHERE table_name='zoom_table' and "
                         f"column_name='{col_name}'")
        records = self.execute_select(sql_text, values_tuple)
        if len(records) == 0:
            # Если такого столбца нет - добавить его
            sql_text = f"ALTER TABLE public.zoom_table ADD COLUMN {col_name} integer;"
            values_tuple = None
            self.logger.info(f"ALTER TABLE public.zoom_table ADD COLUMN {col_name} integer;")
            self.execute_dml(sql_text, values_tuple)
        else:
            # Если столбец уже есть - обнулить его
            sql_text = f"update zoom_table set {col_name}=null;"
            values_tuple = None
            self.logger.info(f"update zoom_table set {col_name}=null;")
            self.execute_dml(sql_text, values_tuple)

    def mark_zoom_attendance(self, col_name, pid, participant):
        count = 0
        self.logger.info(f"Отмечаем присутствие {col_name}|{pid}")
        for i in pid:
            # Можно проставлять суммарное время, только столбец должен быть integer и время не правильно ссумируется
            # видно из-за дублирования или проставлять какой-то символ
            # ВАРИАНТ 1: столбец типа integer
            self.logger.info(
                f"UPDATE public.zoom_table SET {col_name}=coalesce({col_name}, 0)+{participant[4]} WHERE id={i[0]};")
            sql_text = f"UPDATE public.zoom_table SET {col_name}=coalesce({col_name}, 0)+%s WHERE id=%s;"
            values_tuple = (participant[4], i[0])
            # ВАРИАНТ 2: столбец типа varchar
            # sql_text = f"UPDATE public.zoom_table SET {col_name}='+' WHERE id=%s;"
            # values_tuple = (pid,)
            # DEBUG
            # self.logger.info(values_tuple)
            self.execute_dml(sql_text, values_tuple)
            count += 1
        return count

    ################################################################
    def find_zoom_participant_by(self, participant):
        """
        Поиск участника zoom на соотвествие члену команды
        :param participant: Кортеж участника
        :return: [(405,)]
        """
        records = []
        # Ищем сначала по email, если она есть она сразу в lower
        if participant[1]:
            sql_text = "select member_id from zoom_join_zoom_and_members where zoom_email=%s;"
            values_tuple = (participant[1],)
            self.logger.info(f"select member_id from zoom_join_zoom_and_members where zoom_email='{participant[1]}';")
            records = self.execute_select(sql_text, values_tuple)
        # Если по email не нашлось ищем по zoom_name
        if len(records) == 0:
            sql_text = "select member_id from zoom_join_zoom_and_members where zoom_name=%s;"
            values_tuple = (participant[0],)
            self.logger.info(f"select member_id from zoom_join_zoom_and_members where zoom_name='{participant[0]}';")
            records = self.execute_select(sql_text, values_tuple)
            # Если по email и по zoom_name ничего не нашлось, последняя попытка поискать по нормализованному
            # zoom_name это позволит обойти опечатки или двойные пробелы или т.п.
            if len(records) == 0:
                sql_text = "select member_id from zoom_join_zoom_and_members where zoom_name_norm=%s;"
                zoom_name_norm = utils.str_normalization1(participant[0])
                values_tuple = (zoom_name_norm,)
                self.logger.info(
                    f"select member_id from zoom_join_zoom_and_members where zoom_name_norm='{zoom_name_norm}';")
                records = self.execute_select(sql_text, values_tuple)
        if len(records) == 0:
            res = None  # Ничего не нашлось
        else:
            res = set(records)
        # print(f"par={participant}")
        # print(f"rec={records}")
        # print(f"res={res}")
        return res

    def find_participant_by(self, criterion, value):
        """
        Find participant by email or telegram or fio or fio_eng
        :param criterion: Search criteria
        :param value: Search value
        :return: None - if search nothing or ID participant and his type
        """
        self.logger.info(">>>>Class_DBPostgres.find_participant_by begin")
        participant = {
            'id': None,
            'type': None,
            'deadline': None,
            'until_date': None,
            'email': None,
            'telegram': None,
            'login': None,
            'password': None,
            'login1': None,
            'sf_level': None,
            'password1': None
        }
        if value is None or not value:
            self.logger.warning(f"{criterion} отсутствует. Поиск по {criterion} невозможен")
            self.logger.info(">>>>Class_DBPostgres.find_participant_by end")
            return participant  # None
        else:
            # Нормализация value под БД
            if criterion != 'id':
                if criterion == 'email':
                    value = value.lower()
                elif criterion == 'telegram':
                    value = value.lower()
                elif criterion == 'fio':
                    value = value.upper()
                elif criterion == 'fio_eng':
                    value = value.upper()
                else:
                    self.logger.error(f"Это неизвестный критерий поиска участника - {criterion}={value}")
                    raise
            self.logger.info(f"Осуществляем поиск участника по {criterion}={value}")
            # Искать нужно с любым type т.к. заблокированный участник тоже может вновь оплатить
            sql_text = f"select id, type, deadline, until_date, email, telegram, login, password, login1, sf_level, password1 from participants where {criterion}=%s;"
            values_tuple = (value,)
            records = self.execute_select(sql_text, values_tuple)
            # print(records)
            if len(records) > 1:
                self.logger.error(
                    f"Поиск участника по {criterion}={value} возвращает больше одной строки. Возможно дублирование!")
                raise
            elif len(records) == 0:
                participant = participant  # None
            else:
                participant = {
                    'id': records[0][0],
                    'type': records[0][1],
                    'deadline': records[0][2],
                    'until_date': records[0][3],
                    'email': records[0][4],
                    'telegram': records[0][5],
                    'login': records[0][6],
                    'password': records[0][7],
                    'login1': records[0][8],
                    'sf_level': records[0][9],
                    'password1': records[0][10]
                }
            self.logger.debug(f"participant type={type(participant)}")
            self.logger.debug(f"participant={participant}")
            self.logger.info(">>>>Class_DBPostgres.find_participant_by end")
            return participant

    def find_participant_by_telegram_username(self, value):
        """
        Find participant by email or telegram or fio or fio_eng
        :param value: Search value
        :return: None - if search nothing or ID participant and his type
        """
        # Нормализация value под БД
        value = value.lower()
        self.logger.info(f"Осуществляем поиск участника по telegram username={value}")
        # Искать нужно с любым type т.к. заблокированный участник тоже может вновь оплатить
        sql_text = "select id, telegram_id, last_name, first_name, login, password from participants where telegram=%s;"
        values_tuple = (value,)
        records = self.execute_select(sql_text, values_tuple)
        # print(records)
        if len(records) > 1:
            raise Exception(
                f"Поиск участника по telegram username={value} возвращает больше одной строки. Возможно дублирование!")
        elif len(records) == 0:
            person = None
        else:
            person = {
                'id': records[0][0],
                'telegram_id': records[0][1],
                'last_name': records[0][2],
                'first_name': records[0][3],
                'login': records[0][4],
                'password': records[0][5]
            }
        return person

    def disconnect(self):
        self.conn.close()


if __name__ == "__main__":
    import core.custom_logger as custom_logger
    import os

    program_file = os.path.realpath(__file__)
    logger1 = custom_logger.get_logger(program_file=program_file)

    postgres = DBPostgres(dbname=PASSWORDS.settings['postgres_dbname'], user=PASSWORDS.settings['postgres_user'],
                          logger=logger1,
                          password=PASSWORDS.settings['postgres_password'], host=PASSWORDS.settings['postgres_host'],
                          port=PASSWORDS.settings['postgres_port'])

    # id2 = postgres.find_participant_by('email', 'xxxx@gmail.com')
    # id3 = postgres.find_participant_by('telegram', '@xxxx')
    # id4 = postgres.find_participant_by('fio', 'xxxx')
    # id5 = postgres.find_participant_by('fio_eng', 'xxxx')
    # print(f"id2={id2}, id3={id3}, id4={id4}, id5={id5}")

    p = (
        'Иванов Иван', '', datetime.datetime(2020, 4, 10, 20, 48, 52), datetime.datetime(2020, 4, 10, 20, 59, 32),
        11,
        305)
    res1 = postgres.find_zoom_participant_by(p)
    print(res1)

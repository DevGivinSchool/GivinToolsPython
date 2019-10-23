import psycopg2
import logging


class DBPostgres:

    def __init__(self, dbname, host, logger=logging.getLogger('DBPostgres'), port='5432', user='postgres', password='postgres'):
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
        # print(cursor.mogrify(sql_text, values_tuple))
        cursor.execute(sql_text, values_tuple)
        records = cursor.fetchall()
        # print(cursor.rowcount)
        cursor.close()
        return records

    # TODO Переписать все функции в этом файле через execute_dml
    def execute_dml(self, sql_text, values_tuple):
        """Execute DML operations
                   :param values_tuple: Values
                   :param sql_text: Query text.
                   :return result: (Rows count, ID)"""
        cursor = self.conn.cursor()
        # print(cursor.mogrify(sql_text, values_tuple))
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        # print(cursor.rowcount)
        cursor.close()
        return cursor.rowcount

    def execute_dml_id(self, sql_text, values_tuple):
        """Execute DML operations
                   :param values_tuple:
                   :param sql_text: Query text.
                   :return: Count ID"""
        cursor = self.conn.cursor()
        # print(cursor.mogrify(sql_text, values_tuple))
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

    def create_task(self, session_id, task):
        """
        Create new task. If the task already exist, then increase attempt count.
        :param session_id:
        :param task:
        :return: True - It is new task; False - It is reprocessing task
        """
        try:
            cursor = self.conn.cursor()
            sql_text = """INSERT INTO tasks 
            (time_begin, task_from, task_subject, task_body_type, task_body_html, task_body_text,
             task_uuid, session_id) VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s) RETURNING task_uuid;"""
            values_tuple = (task.ffrom, task.subject, task.body['body_type'], task.body['body_html'],
                            task.body['body_text'], task.uuid, session_id)
            cursor.execute(sql_text, values_tuple)
        except psycopg2.errors.UniqueViolation as e:
            """ If that row already exist, than update attempts"""
            self.conn.rollback()
            cursor.close()
            # print("="*45)
            # print("psycopg2.Error::")
            # print(e.pgerror)
            # print(e.diag.message_detail)
            try:
                cursor = self.conn.cursor()
                sql_text = """UPDATE tasks set attempt = attempt + 1 where task_uuid=%s;"""
                values_tuple = (task.uuid,)
                cursor.execute(sql_text, values_tuple)
                self.conn.commit()
                return False
            except Exception as e:
                raise
        try:
            sql_text = """INSERT INTO sessions_tasks(task_uuid, session_id) VALUES (%s, %s);"""
            values_tuple = (task.uuid, session_id)
            cursor.execute(sql_text, values_tuple)
        except Exception as e:
            raise
        self.conn.commit()
        # task_uuid_ = cursor.fetchone()[0]
        cursor.close()
        return True

    def session_begin(self):
        cursor = self.conn.cursor()
        sql_text = """INSERT INTO sessions(time_begin) VALUES (NOW()) RETURNING id;"""
        cursor.execute(sql_text)
        self.conn.commit()
        id_ = cursor.fetchone()[0]
        cursor.close()
        return id_

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

    def create_payment(self, task):
        """
        Создание платежа. К платежу сразу привязывается плательщик, если находится соответсвие по почте или ФИО
        :param task:
        :return:
        """
        # participant_id = self.find_participant(task.payment["Электронная почта"], task.payment["Фамилия Имя"])
        # TODO Реализовать поиск по fio_eng
        # Ищем участника сначала по email
        self.logger.info(f"Ищем участника сначала по email - {task.payment['Электронная почта']}")
        participant_id, p_type = self.find_participant_by('email', task.payment["Электронная почта"])
        if participant_id is None:
            # Ищем по fio
            self.logger.info(f"Ищем участника по fio - {task.payment['Фамилия Имя']}")
            participant_id, p_type = self.find_participant_by('fio', task.payment["Фамилия Имя"])
        cursor = self.conn.cursor()
        sql_text = """INSERT INTO payments(task_uuid, name_of_service, payment_id, amount, participant_id, 
        sales_slip, card_number, card_type, payment_purpose, last_name, first_name, fio, email, payment_system) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING task_uuid;"""
        values_tuple = (task.uuid, task.payment["Наименование услуги"], task.payment["ID платежа"],
                        task.payment["Оплаченная сумма"], participant_id, task.payment["Кассовый чек 54-ФЗ"],
                        task.payment["Номер карты"], task.payment["Тип карты"], 1, task.payment["Фамилия"],
                        task.payment["Имя"], task.payment["Фамилия Имя"], task.payment["Электронная почта"],
                        task.payment["Платежная система"])
        # print(values_tuple)
        self.logger.debug(f'values_tuple={values_tuple}')
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        id_ = cursor.fetchone()[0]
        cursor.close()
        return id_, participant_id

    ################################################################

    def find_participant_by(self, criterion, value):
        """
        Find participant by email or telegram or fio or fio_eng
        :param criterion: Search criteria
        :param value: Search value
        :return: None - if search nothing or ID participant and his type
        """
        if value is None or not value:
            self.logger.warning(f"{criterion} отсутствует. Поиск по {criterion} невозможен")
            return None, None
        else:
            # Нормализация value под БД
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
            sql_text = f"""select id, type from participants where {criterion}=%s; """
            values_tuple = (value,)
            records = self.execute_select(sql_text, values_tuple)
            # print(records)
            if len(records) > 1:
                raise (f"Поиск участника по {criterion}={value} "
                       f"возвращает больше одной строки. Возможно дублирование.")
            elif len(records) == 0:
                id_ = None
                type_ = None
            else:
                id_ = records[0][0]
                type_ = records[0][1]
            return id_, type_

    def disconnect(self):
        self.conn.close()


if __name__ == "__main__":
    import config
    import PASSWORDS

    postgres = DBPostgres(dbname=config.config['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                          password=PASSWORDS.logins['postgres_password'], host=config.config['postgres_host'],
                          port=config.config['postgres_port'])

    id2 = postgres.find_participant_by('email', 'tikitikishik@gmail.com')
    id3 = postgres.find_participant_by('telegram', '@rikitikishik')
    id4 = postgres.find_participant_by('fio', 'ЛОГИНОВА ДАРЬЯ')
    id5 = postgres.find_participant_by('fio_eng', 'MILA KIM VULFOV')


    # id2 = postgres.find_participant_test("ivan@mail.ru")
    # id2 = postgres.find_participant_test("@ivan")
    # id2 = postgres.find_participant_test("ИВАНОВ ИВАН")
    print(f"id2={id2}, id3={id3}, id4={id4}, id5={id5}")

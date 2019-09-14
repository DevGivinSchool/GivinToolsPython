import psycopg2
from uuid import uuid4
from contextlib import closing
import config
import PASSWORDS
import Task


class DBPostgres:

    def __init__(self, dbname, host, port='5432', user='postgres', password='postgres'):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password,
                                     host=self.host, port=self.port)

    def execute_select(self, sql_text):
        """Execute selects
           :param sql_text: Query text.
           :return: List of tuples = List of strings"""
        cursor = self.conn.cursor()
        cursor.execute(sql_text)
        records = cursor.fetchall()
        cursor.close()
        return records

    def execute_dml(self, sql_text):
        """Execute DML operations
                   :param sql_text: Query text.
                   :return: Count rows"""
        cursor = self.conn.cursor()
        cursor.execute(sql_text)
        self.conn.commit()
        count = cursor.rowcount
        cursor.close()
        return count

    def execute_dml_id(self, sql_text):
        """Execute DML operations
                   :param sql_text: Query text.
                   :return: Count ID"""
        cursor = self.conn.cursor()
        cursor.execute(sql_text)
        self.conn.commit()
        id_ = cursor.fetchone()[0]
        cursor.close()
        return id_

    def create_task(self, session_id, task):
        cursor = self.conn.cursor()
        sql_text = """INSERT INTO tasks 
        (time_begin, task_from, task_subject, task_body_type, task_body_html, task_body_text,
         task_uuid, session_id) VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s) RETURNING task_uuid;"""
        values_tuple = (task.ffrom, task.subject, task.body['body_type'], task.body['body_html'],
                        task.body['body_text'], task.uuid, session_id)
        # cursor.execute(sql_text, values_tuple)

        try:
            cursor.execute(sql_text, values_tuple)
        except psycopg2.errors.UniqueViolation as e:
            print("="*45)
            print("psycopg2.Error::")
            print(e.pgerror)
            print(e.diag.message_detail)
            raise




        self.conn.commit()
        task_uuid_ = cursor.fetchone()[0]
        cursor.close()
        return task_uuid_

    def session_begin(self):
        cursor = self.conn.cursor()
        sql_text = """INSERT INTO sessions(time_begin) VALUES (NOW()) RETURNING id;"""
        cursor.execute(sql_text)
        self.conn.commit()
        id_ = cursor.fetchone()[0]
        cursor.close()
        return id_

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
        participant_id = self.find_participant(task)
        if participant_id == 0:
            participant_id = None
        cursor = self.conn.cursor()
        sql_text = """INSERT INTO payments(task_uuid, name_of_service, payment_id, amount, participant_id
         sales_slip, card_number, card_type, payment_purpose, last_name, first_name, fio, email, payment_system) 
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        values_tuple = (task.uuid, task.payment["Наименование услуги"], task.payment["ID платежа"],
                        task.payment["Оплаченная сумма"], participant_id, task.payment["Кассовый чек 54-ФЗ"],
                        task.payment["Номер карты"], task.payment["Тип карты"], 1, task.payment["Фамилия"],
                        task.payment["Имя"], task.payment["Фамилия Имя"], task.payment["Электронная почта"],
                        task.payment["Платежная система"])
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        id_ = cursor.fetchone()[0]
        cursor.close()
        return id_

    def find_participant(self, task):
        """Find participant by email and FIO"""
        cursor = self.conn.cursor()
        # Find by email
        sql_text = """select id from participants where email=%s;"""
        values_tuple = (task.payment["Электронная почта"],)
        cursor.execute(sql_text, values_tuple)
        data = cursor.fetchone()
        id_ = 0
        if data is not None:
            id_ = data[0]
            return id_
        """
        # Find by Telegram (in task is not telegram)
        sql_text = "select id from participants where telegram=%s;"
        values_tuple = (TELEGRAM,)
        cursor.execute(sql_text, values_tuple)
        data = cursor.fetchone()
        if data is not None:
            id_ = data[0]
            return id_
        """
        # Find by FIO (even a complete match cannot guarantee reliability, because may be namesakes)
        sql_text = """select id from participants where fio=%s;"""
        values_tuple = (task.payment["Фамилия Имя"],)
        cursor.execute(sql_text, values_tuple)
        if cursor.rowcount == 1:
            data = cursor.fetchone()
            if data is not None:
                id_ = data[0]
                return id_
        cursor.close()
        return id_

    def disconnect(self):
        self.conn.close()

    def find_participant_test(self, value):
        """"""
        cursor = self.conn.cursor()
        # Find by email
        sql_text = """select id from participants where email=%s;"""
        values_tuple = (value,)
        cursor.execute(sql_text, values_tuple)
        data = cursor.fetchone()
        id_ = 0
        if data is not None:
            id_ = data[0]
            return id_
        # Find by Telegram
        sql_text = """select id from participants where telegram=%s;"""
        values_tuple = (value,)
        cursor.execute(sql_text, values_tuple)
        data = cursor.fetchone()
        if data is not None:
            id_ = data[0]
            return id_
        # Find by FIO (even a complete match cannot guarantee reliability, because may be namesakes)
        sql_text = """select id from participants where fio=%s;"""
        values_tuple = (value,)
        cursor.execute(sql_text, values_tuple)
        if cursor.rowcount == 1:
            data = cursor.fetchone()
            if data is not None:
                id_ = data[0]
                return id_
        cursor.close()
        return id_


if __name__ == "__main__":
    import config
    import PASSWORDS
    postgres = DBPostgres(dbname=config.config['postgres_dbname'], user=PASSWORDS.logins['postgres_user'],
                          password=PASSWORDS.logins['postgres_password'], host=config.config['postgres_host'],
                          port=config.config['postgres_port'])

    # id2 = postgres.find_participant_test("sa_azarov@mail.ru")
    # id2 = postgres.find_participant_test("@azarov_sa")
    id2 = postgres.find_participant_test("АЗАРОВ СЕРГЕЙ")
    print(id2)

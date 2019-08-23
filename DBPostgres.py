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

    def insert_task(self, session_id, task):
        cursor = self.conn.cursor()
        sql_text = """INSERT INTO tasks 
        (time_begin, task_from, task_subject, task_body_type, task_body_html, task_body_text,
         task_uuid, session_id) VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s);"""
        values_tuple = (task.ffrom, task.subject, task.body['body_type'], task.body['body_html'],
                        task.body['body_text'], task.uuid, session_id)
        cursor.execute(sql_text, values_tuple)
        self.conn.commit()
        count = cursor.rowcount
        cursor.close()
        return count

    def disconnect(self):
        self.conn.close()

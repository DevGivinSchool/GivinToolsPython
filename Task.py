import yandex_mail
import yandex_connect
import password_generator


class Task:
    """Kласс для задачи"""

    def __init__(self, uuid, ffrom, subject, body, logger, database, payment={}, attr={}):
        """:param uuid: Уникальный номер задачи, совпадает с UID письма.
           :param ffrom: От кого письмо и кому отвечать после выполнения задачи.
           :param subject: Тема письма, здесь может содержаться команда.
           :param body: Тело письма.
           :param logger: Лог файл для этой задачи.
           :param attr: Словарь дополнительных аттрибутов.

        """
        self.uuid = uuid
        self.ffrom = ffrom
        self.subject = subject
        self.body = body
        self.database = database
        self.logger = logger
        self.payment = payment
        self.attr = attr
        self.login_ = None
        self.password_ = None

        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

    def display_task(self):
        print(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')
        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

    def task_run(self):
        """
        Обработка платежа, пока без обработки шагов
        :return:
        """
        self.logger.info('Task_run begin')
        self.logger.info(f'task_run payment = {self.payment}')
        if self.payment["participant_id"] is None:
            # This is new participant
            # Participant must have Name, Surname, Email
            if self.payment["Фамилия"] is None or not self.payment["Фамилия"]:
                self.logger.error("The participant must have a Surname")
                raise Exception("The participant must have a Surname")
            if self.payment["Имя"] is None or not self.payment["Имя"]:
                self.logger.error("The participant must have a Name")
                raise Exception("The participant must have a Name")
            if self.payment["Электронная почта"] is None \
                    or not self.payment["Электронная почта"]:
                self.logger.error("The participant must have a Email")
                raise Exception("The participant must have a Email")
            # Создаём нового пользователя в БД
            sql_text = """INSERT INTO participants(last_name, first_name, fio, email) VALUES (%s, %s, %s, %s);"""
            values_tuple = (self.payment["Фамилия"], self.payment["Имя"],
                            self.payment["Фамилия Имя"], self.payment["Электронная почта"])
            participants_create_result = self.database.execute_dml(self, sql_text, values_tuple)
            print(type(participants_create_result))
            print(participants_create_result)
            print(participants_create_result[1])
            self.logger.info(type(participants_create_result))
            self.logger.info(participants_create_result)
            self.logger.info(participants_create_result[1])
            # Отмечаем оплату в БД
            self.mark_payment_into_db()
            # Создаём почту новому пользователю в домене @givinschool.org
            try:
                result = yandex_mail.create_yandex_mail(self.payment["Фамилия"], self.payment["Имя"], department_id_=4)
                # print(f"Email created:{result['email']}")
                self.login_ = result['email']
                self.logger.info(f"Email created:{self.login_}")
                # Отдел 4 = @ДРУЗЬЯ_ШКОЛЫ
            except yandex_connect.YandexConnectExceptionY as e:
                # print(e.args[0])
                if e.args[0] == 500:
                    print(f'Unhandled exception: Такая почта уже существует: '
                          f'{self.payment["Фамилия"] + "_" + self.payment["Имя"] + "@givinschool.org"}')
                    self.logger.info(f'Unhandled exception: Такая почта уже существует: '
                                     f'{self.payment["Фамилия"] + "_" + self.payment["Имя"] + "@givinschool.org"}')
                else:
                    raise
            # Генерация пароля для Zoom (для всех почт пароль одинаковый)
            self.password_ = password_generator.random_password(strong=True)
            self.logger.info(f"Password:{self.password_}")
            sql_text = """UPDATE participants SET login=%s, password=%s WHERE id=%s;"""
            values_tuple = (self.login_, self.password_, participants_create_result[1])
            self.database.execute_dml(sql_text, values_tuple)
            # TODO Написать письмо пользователю
            # TODO Написать письмо админу чтобы создал Zoom учётку.
        else:
            # Отмечаем оплату в БД
            self.mark_payment_into_db()
            # TODO Если пользователь был заблокированным, тогда:
                # TODO Написать письмо пользователю
                # TODO Написать письмо админу чтобы разблокировал Zoom учётку.
            pass

        self.logger.info('Task_run end')

    def mark_payment_into_db(self):
        """
        Отмечаем оплату в БД. Поле until_date (отсрочка до) обнуляется.
        :return:
        """
        self.logger.info("Отмечаем оплату в БД")
        # Коментарий и поле отсрочки обнуляются
        sql_text = """UPDATE participants 
        SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type='P' 
        WHERE id=%s;"""
        values_tuple = (self.payment["Время проведения"], self.payment["number_of_days"],
                        self.payment["deadline"], self.payment["participant_id"])
        self.database.execute_dml(sql_text, values_tuple)

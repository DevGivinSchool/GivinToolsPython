import yandex_mail
import yandex_connect
import password_generator
import PASSWORDS
import zoom_us
from utils import get_login
from alert_to_mail import send_mail


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
                self.logger.error("+" * 60)
                self.logger.error("The participant must have a Email!!!")
                self.logger.error("+" * 60)
                # raise Exception("The participant must have a Email")

            # Создаём нового пользователя в БД
            self.logger.info(f"Создаём нового пользователя в БД ({self.payment['fio_lang']})")
            if self.payment["fio_lang"] == "RUS":
                sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type) 
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
                values_tuple = (self.payment["Фамилия"], self.payment["Имя"],
                                self.payment["Фамилия Имя"], self.payment["Электронная почта"],
                                self.payment["telegram"], 'N')
            else:
                sql_text = """INSERT INTO participants(last_name, first_name, fio, email, telegram, type, last_name_eng, first_name_eng, fio_eng) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
                values_tuple = (self.payment["Фамилия"], self.payment["Имя"],
                                self.payment["Фамилия Имя"], self.payment["Электронная почта"],
                                self.payment["telegram"], 'N',
                                self.payment["Фамилия"], self.payment["Имя"], self.payment["Фамилия Имя"])
            self.payment["participant_id"] = self.database.execute_dml_id(sql_text, values_tuple)
            # print(type(self.payment["participant_id"]))
            # print(self.payment["participant_id"])
            # print(participants_create_result[1])
            # self.logger.info(type(self.payment["participant_id"]))
            # self.logger.info(self.payment["participant_id"])
            # self.logger.info(participants_create_result[1])
            self.logger.info(self.select_participant(self.payment["participant_id"]))

            # Отмечаем оплату в БД этому участнику
            self.mark_payment_into_db(participant_type='N')

            # Прикрепить участника к платежу
            sql_text = """UPDATE payments SET participant_id=%s WHERE task_uuid=%s;"""
            values_tuple = (self.payment["participant_id"], self.payment["task_uuid"])
            self.database.execute_dml(sql_text, values_tuple)
            self.logger.info(self.select_payment(self.payment["task_uuid"]))

            # Создаём почту новому участнику в домене @givinschool.org
            self.logger.info("Создаём почту новому участнику в домене @givinschool.org")
            login_ = get_login(self.payment["Фамилия"], self.payment["Имя"])
            try:
                result = yandex_mail.create_yandex_mail(self.payment["Фамилия"], self.payment["Имя"], login_,
                                                        department_id_=4)
                # print(f"Email created:{result['email']}")
                self.login_ = result['email']
                self.logger.info(f"Email created: {self.login_}")
                # Отдел 4 = @ДРУЗЬЯ_ШКОЛЫ
            except yandex_connect.YandexConnectExceptionY as e:
                # print(e.args[0])
                if e.args[0] == 500:
                    print(f'Unhandled exception: Такая почта уже существует: '
                          f'{login_ + "@givinschool.org"}')
                    self.logger.info(f'Unhandled exception: Такая почта уже существует: '
                                     f'{login_ + "@givinschool.org"}')
                else:
                    raise
            # Для удобства создания учётки zoom записать в лог фамилию и имя
            self.logger.info(f"Фамилия: {self.payment['Фамилия'].title()}")
            self.logger.info(f"Имя: {self.payment['Имя'].title()}")
            # Генерация пароля для Zoom (для всех почт пароль одинаковый)
            self.password_ = password_generator.random_password(strong=True, zoom=True)
            self.logger.info(f"Password: {self.password_}")
            self.logger.info("Обновляем участнику логин и пароль в БД")
            sql_text = """UPDATE participants SET login=%s, password=%s WHERE id=%s;"""
            values_tuple = (self.login_, self.password_, self.payment["participant_id"])
            self.database.execute_dml(sql_text, values_tuple)
            self.logger.info(self.select_participant(self.payment["participant_id"]))

            # Создание учётки Zoom участнику
            self.logger.info("Создание учётки Zoom участнику")
            mail_text = ""
            subject = "SEND TELEGRAM"
            zoom_result = zoom_us.zoom_users_create(self.login_, self.payment['Имя'].title(),
                                                    self.payment['Фамилия'].title(), self.password_, logger=self.logger)
            if zoom_result is not None:
                self.logger.error("+" * 60)
                subject = "CREATE ZOOM ERROR"
                mail_text = f"\nПроцедура не смогла создать учётку Zoom с ошибкой:\n" \
                            f"{zoom_result}\n\n" \
                            f"Создать учётку zoom участнику\nID={self.payment['participant_id']}\n" \
                            f"{self.payment['Фамилия'].title()}\n{self.payment['Имя'].title()}\n" \
                            f"Login: {self.login_}\nPassword: {self.password_}\n" \
                            f"Сведения по участнику и платежу можно посмотреть по ссылке - " \
                            f"{self.payment['Кассовый чек 54-ФЗ']}"
                self.logger.error(mail_text)
                self.logger.error("+" * 60)
            else:
                self.logger.info("Учётка Zoom успешно создана")
            # TODO Отправить Telegram участнику
            self.logger.warning("+" * 60)
            self.logger.info("TODO: Отправить уведомление участнику в Telegram.")
            mail_text += f"\nОтправить Telegram участнику {self.payment['telegram']}"
            send_mail(PASSWORDS.logins['admin_emails'], subject, mail_text, self.logger)
            self.logger.warning("+" * 60)
            self.participant_notification()
        else:
            # Отмечаем оплату в БД
            self.mark_payment_into_db()
        self.logger.info('Task_run end')

    def participant_notification(self):
        self.logger.info("Уведомление участника")
        mail_text2 = f"""Здравствуйте, {self.payment['Фамилия Имя'].title()}!  

Поздравляем, Вы оплатили абонемент на месяц совместных занятий в онлайн-формате "Друзья Школы Гивина". 

Ваш zoom-аккаунт:
Логин: {self.login_}
Пароль: {self.password_}

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
        self.logger.info(mail_text2)
        send_mail([self.payment["Электронная почта"]],
                  r"[ШКОЛА ГИВИНА]. Поздравляем, Вы приняты в Друзья Школы", mail_text2, self.logger)

    def mark_payment_into_db(self, participant_type='P'):
        """
        Отмечаем оплату в БД. Поля until_date (отсрочка до) и comment - обнуляются.
        :return:
        """
        self.logger.info("Отмечаем оплату в БД")
        # Состояние участника до отметки
        self.logger.info(self.select_participant(self.payment["participant_id"]))
        # Коментарий и поле отсрочки обнуляются
        # Для заблокированного пользователя меняется его тип (type) и из пароля удаляются два последних символа
        if self.payment["participant_type"] == "B":
            # Нужно дополнить сведения участника которых не хватает (т.к. это не новый участник а заблокированный)
            result = self.database.get_participant_by_id(self.payment["participant_id"])[0]
            self.payment["Фамилия"] = result[0]
            self.payment["Имя"] = result[1]
            self.payment["Фамилия Имя"] = result[2]
            self.payment["Электронная почта"] = result[3]
            self.payment["telegram"] = result[4]
            self.login_ = result[5]
            self.password_ = result[6]
            # [('ИВАНОВ', 'ИВАН', 'ИВАНОВ ИВАН', 'xxx@mail.ru', '@xxxx', 'ivanov_ivan@givinschool.org', '43RFji1r48')]
            # Исправление пароля (вырезать 55 в конце)
            if self.password_[-2:] == "55":
                self.password_ = self.password_[:-2]
            self.logger.info("Разблокировка пользователя")
            sql_text = """UPDATE participants 
            SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type=%s, password=%s
            WHERE id=%s;"""
            values_tuple = (self.payment["Время проведения"], self.payment["number_of_days"],
                            self.payment["deadline"], participant_type, self.password_, self.payment["participant_id"])
            # Измение статуса в zoom
            zoom_result = zoom_us.zoom_userstatus(self.login_, "activate", logger=self.logger)
            if zoom_result is not None:
                self.logger.error("+" * 60)
                mail_text = f"\nПроцедура не смогла автоматически разблокировать участника. Ошибка:\n" \
                            f"{zoom_result}" \
                            f"ID={self.payment['participant_id']}\n{self.payment['Фамилия Имя']}:" \
                            f"\nLogin: {self.login_}\nPassword: {self.password_}"
                send_mail(PASSWORDS.logins['admin_emails'], "UNBLOCK PARTICIPANT ERROR", mail_text, self.logger)
                self.logger.error(mail_text)
                self.logger.error("+" * 60)
            else:
                self.logger.info("Учётка Zoom успешно активирована")

            self.participant_notification()
        else:
            sql_text = """UPDATE participants 
            SET payment_date=%s, number_of_days=%s, deadline=%s, until_date=NULL, comment=NULL, type=%s 
            WHERE id=%s;"""
            values_tuple = (self.payment["Время проведения"], self.payment["number_of_days"],
                            self.payment["deadline"], participant_type, self.payment["participant_id"])
        # self.logger.info(sql_text % values_tuple)
        self.database.execute_dml(sql_text, values_tuple)
        # Состояние участника после отметки
        self.logger.info(self.select_participant(self.payment["participant_id"]))

    def select_participant(self, participant_id):
        sql_text = 'SELECT * FROM participants where id=%s;'
        values_tuple = (participant_id,)
        rows = self.database.execute_select(sql_text, values_tuple)
        return rows

    def select_payment(self, task_uuid):
        sql_text = 'SELECT * FROM payments where task_uuid=%s;'
        values_tuple = (task_uuid,)
        rows = self.database.execute_select(sql_text, values_tuple)
        return rows

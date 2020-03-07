import yandex_mail
import yandex_connect
import password_generator
import PASSWORDS
import zoom_us
import gtp_participant_create
from utils import get_login
from alert_to_mail import send_mail


class Task:
    """Kласс для задачи"""

    def __init__(self, uuid, ffrom, subject, logger, database, payment={}):
        """:param uuid: Уникальный номер задачи, совпадает с UID письма.
           :param ffrom: От кого письмо и кому отвечать после выполнения задачи.
           :param subject: Тема письма, здесь может содержаться команда.
        #   :param body: Тело письма.
           :param logger: Лог файл для этой задачи.
        #  :param attr: Словарь дополнительных аттрибутов.
        """
        self.uuid = uuid
        self.ffrom = ffrom
        self.subject = subject
        # self.body = body
        self.database = database
        self.logger = logger
        self.payment = payment
        # self.attr = attr
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
            gtp_participant_create.create_sf_participant(self.payment, self.database, self.logger)
        else:
            # Отмечаем оплату в БД
            gtp_participant_create.mark_payment_into_db(self.payment, self.database, self.logger)
        self.logger.info('Task_run end')

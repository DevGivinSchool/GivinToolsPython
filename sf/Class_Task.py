from . import sf_participant_create


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
        self.logger.info('>>>>task_run begin')
        self.logger.info(f'task_run payment = \n{self.payment}')
        if self.payment["participant_id"] is None:
            # This is new participant
            self.logger.info('СОЗДАЁМ НОВОГО ПОЛЬЗОВАТЕЛЯ')
            sf_participant_create.create_sf_participant(self.payment, self.database, self.logger)
        else:
            # Отмечаем оплату в БД
            self.logger.info('ОТМЕЧАЕМ ОПЛАТУ В БД')
            # Участник оплатил 2 уровень но такой учётки у него еще нет и это особый случай special_case=True
            if self.payment["level"] == 2 and not self.payment["login"]:
                self.logger.info('ЭТО ОСОБЫЙ СЛУЧАЙ переход с level1 на level2')
                sf_participant_create.create_sf_participant(self.payment, self.database, self.logger, special_case=True)
            sf_participant_create.mark_payment_into_db(self.payment, self.database, self.logger)
        self.logger.info('>>>>task_run end')

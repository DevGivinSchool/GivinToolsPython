class Task:
    """Kласс для задачи"""

    def __init__(self, uuid, ffrom, subject, body, logger, payment={}, attr={}):
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
        self.logger = logger
        self.payment = payment
        self.attr = attr

        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

    def display_task(self):
        print(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')
        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

    def task_run(self):
        """
        Обработка платежа, пока без обработки шагов
        :return:
        """
        self.logger.info('Payment processing begin')
        self.logger.info(f'task_run payment = {self.payment}')
        if self.payment["participant_id"] is None:
            # This is new participant
            # TODO Здесь нужно завести нового пользователя
            pass
        else:
            # TODO Здесь нужно проставить отметку уже существующему участнику
            pass

        self.logger.info('Payment processing end')

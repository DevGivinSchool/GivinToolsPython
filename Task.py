import Parser

class Task:
    """Kласс для задачи"""

    def __init__(self, uuid, ffrom, subject, body, logger, attr={}):
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
        self.attr = attr

        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

    def display_task(self):
        print(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')
        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

    def run_task(self):
        if self.ffrom == 'noreply@server.paykeeper.ru' and self.subject == 'Принята оплата':
            self.logger.debug(f'Это письмо от платежной системы - PayKeepre')
            print(f'Это письмо от платежной системы - PayKeepre')
            Parser.parse_paykeeper_html(self.body['body_html'])
        elif self.ffrom == 'no-reply@getcourse.ru' and self.subject.startswith("Поступил платеж"):
            self.logger.debug(f'Это письмо от платежной системы - GetCourse')
            print(f'Это письмо от платежной системы - GetCourse')
            Parser.parse_getcourse_html(self.body['body_html'])
        # Здесь из письма нужно вытащить сведения о пользователе и платеже.
        else:
            self.logger.debug(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
            print(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')

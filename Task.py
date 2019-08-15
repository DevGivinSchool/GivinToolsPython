class Task:
    """Kласс для задачи"""

    def __init__(self, uuid, ffrom, subject, body, logger):
        self.uuid = uuid
        self.ffrom = ffrom
        self.subject = subject
        self.body = body
        self.logger = logger
        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

    def display_task(self):
        print(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')
        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

    def run_task(self):
        if (self.ffrom == 'noreply@server.paykeeper.ru' and self.subject == 'Принята оплата') or \
           (self.ffrom == 'no-reply@getcourse.ru' and self.subject.startswith("Поступил платеж")):
            self.logger.debug(f'Это письмо от платежных систем - обработать')
            print(f'Это письмо от платежных систем - обработать')

        else:
            self.logger.debug(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
            print(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')

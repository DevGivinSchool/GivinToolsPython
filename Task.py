class Task:
    """Kласс для задачи"""

    def __init__(self, uuid, ffrom, subject, body, logger):
        self.uuid = uuid
        self.ffrom = ffrom
        self.subject = subject
        self.body = body
        self.logger = logger

    def display_task(self):
        print(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')
        self.logger.debug(f'Task {self.uuid}:\n   from = {self.ffrom}\n   subject = {self.subject}\n')

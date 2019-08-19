import Parser


def check_school_friends(text):
    """Проверяем что назначение платежа - Друзья школы"""
    text_lower = text.lower()
    list_ofstrs = ['друзья', 'школы']
    # Check if all strings from the list exists in given string
    result = all(([True if sub_str in text_lower else False for sub_str in list_ofstrs]))
    return result


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
        """Определяем нужные письма и из нужных вытаскиваем данные платежа."""
        payment = {}
        # TODO: Нужно результаты обработки писем заносить в БД и потом в Email2 получить сводку и отправлять админу.
        if self.ffrom == 'noreply@server.paykeeper.ru' and self.subject == 'Принята оплата':
            self.logger.debug(f'Это письмо от платежной системы - PayKeeper')
            print(f'Это письмо от платежной системы - PayKeeper')
            payment = Parser.parse_paykeeper_html(self.body['body_html'])
            self.logger.debug(f'payment = {payment}')
            if check_school_friends(payment["Наименование услуги"]):
                print('Это платёж Друзья Школы')
                self.logger.debug('Это платёж Друзья Школы')
                # TODO: Процедура обработки payment
            else:
                print('Это ИНОЙ платёж')
                self.logger.debug('Это ИНОЙ платёж')
                # TODO: Нужно результаты обработки писем заносить в БД и потом в Email2 получить сводку и отправлять админу.
        elif self.ffrom == 'no-reply@getcourse.ru' and self.subject.startswith("Поступил платеж"):
            self.logger.debug(f'Это письмо от платежной системы - GetCourse')
            print(f'Это письмо от платежной системы - GetCourse')
            payment = Parser.parse_getcourse_html(self.body['body_html'])
            self.logger.debug(f'payment = {payment}')
            # TODO: Процедура обработки payment
        else:
            self.logger.debug(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
            print(f'Это письмо НЕ от платежных систем - ничего с ним не делаю, пока...')
            # TODO: Нужно результаты обработки писем заносить в БД и потом в Email2 получить сводку и отправлять админу.
        print('-' * 45)
        return payment

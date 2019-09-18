import yandex_mail
import yandex_connect


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
            # TODO ОТМЕТИТЬ ОПЛАТУ В БД
            pass
            # TODO Создать почту
            try:
                yandex_mail.create_yandex_mail(line[0], line[1], department_id_=4)  # Отдел 4 = @ДРУЗЬЯ_ШКОЛЫ
            except yandex_connect.YandexConnectExceptionY as e:
                # print(e.args[0])
                if e.args[0] == 500:
                    print(f"Unhandled exception: Такой пользователь уже существует: {login_ + '@givinschool.org'}")
                else:
                    print("ERROR = " + e.__str__())
            # Для почты стандартный пароль, это пароль для Zoom
            print(password_generator.randompassword(strong=True))
            # TODO Написать письмо пользователю
            # TODO Написать письмо админу чтобы создал Zoom учётку.
        else:
            # TODO ОТМЕТИТЬ ОПЛАТУ В БД
            # TODO Если пользователь был заблокированным, тогда:
                # TODO Написать письмо пользователю
                # TODO Написать письмо админу чтобы разблокировал Zoom учётку.
            pass

        self.logger.info('Payment processing end')

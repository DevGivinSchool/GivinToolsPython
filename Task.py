import yandex_mail
import yandex_connect
import password_generator

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
        self.logger.info('Task_run begin')
        self.logger.info(f'task_run payment = {self.payment}')
        if self.payment["participant_id"] is None:
            # This is new participant
            # TODO ЗАВЕСТИ НОВОГО ПОЛЬЗОВАТЕЛЯ В БД

            # TODO ОТМЕТИТЬ ОПЛАТУ В БД
            pass
            # TODO Создать почту
            try:
                result = yandex_mail.create_yandex_mail(self.payment["Фамилия"], self.payment["Имя"], department_id_=4)
                print(f"Email created:{result['email']}")
                self.logger.info(f"Email created:{result['email']}")
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
            # Для почты стандартный пароль, это пароль для Zoom
            # TODO Вместо этого нужно занести пароль в БД
            print(password_generator.randompassword(strong=True))
            # TODO Написать письмо пользователю
            # TODO Написать письмо админу чтобы создал Zoom учётку.
        else:
            # TODO ОТМЕТИТЬ ОПЛАТУ В БД
            # TODO Если пользователь был заблокированным, тогда:
                # TODO Написать письмо пользователю
                # TODO Написать письмо админу чтобы разблокировал Zoom учётку.
            pass

        self.logger.info('Task_run end')

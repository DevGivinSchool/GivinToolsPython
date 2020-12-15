import datetime
from django.db import models


# Create your models here.
class Article(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, verbose_name="Название")
    text = models.TextField(verbose_name="Текст")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


##########################################################
# time_begin default=datetime.date.today
# create_date = models.DateTimeField(default=timezone.now)
class Participant(models.Model):
    """
    Участник проекта Друзья Школы
    """
    PARTICIPANT_TYPE_VOC = [
        ('N', 'новый участник (первый месяц)'),
        ('P', 'регулярный участник'),
        ('B', 'заблокированный'),
        ('E', 'наш сотрудник'),
        ('V', 'VIP (особые условия, например, участие без оплаты)'),
    ]
    last_name = models.CharField(blank=True, null=True, max_length=255, verbose_name="Фамилия по русски")
    first_name = models.CharField(blank=True, null=True, max_length=255, verbose_name="Имя по русски")
    fio = models.CharField(blank=True, db_index=True, null=True, max_length=500, verbose_name="Фамилия и Имя по русски")
    email = models.CharField(blank=True, db_index=True, null=True, max_length=254, verbose_name="Email")
    telegram = models.CharField(blank=True, db_index=True, null=True, max_length=32, verbose_name="Telegram name")
    time_begin = models.DateTimeField(null=False, editable=False, auto_now_add=True, verbose_name="Дата создания")
    time_end = models.DateTimeField(blank=True, editable=False, null=True, verbose_name="Дата блокировки")
    login = models.CharField(blank=True, null=True, max_length=100,
                             verbose_name="Логин пользователя в домене @givinschool.org, соответствует почте")
    password = models.CharField(blank=True, null=True, max_length=32, verbose_name="Пароль участника")
    payment_date = models.DateField(blank=True, null=True, default=datetime.date.today, verbose_name="Дата оплаты")
    number_of_days = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Количество оплаченных дней")
    deadline = models.DateField(blank=True, null=True, verbose_name="Дата следующей оплаты")
    comment = models.CharField(blank=True, null=True, max_length=4000, verbose_name="Комментарий")
    until_date = models.DateField(blank=True, null=True, verbose_name="Дата до которой отсрочен платёж")
    type = models.CharField(
        max_length=1,
        choices=PARTICIPANT_TYPE_VOC,
        default='N',
        verbose_name="Тип участника: "
                     "N - новый участник (первый месяц); "
                     "P - регулярный участник; "
                     "B - заблокированный; "
                     "E - наш сотрудник; "
                     "V - VIP (особые условия, например, участие без оплаты)",
    )
    last_name_eng = models.CharField(blank=True, null=True, max_length=255, verbose_name="Фамилия по английски")
    first_name_eng = models.CharField(blank=True, null=True, max_length=255, verbose_name="Имя по английски")
    fio_eng = models.CharField(blank=True, db_index=True, null=True, max_length=500, verbose_name="Фамилия и Имя по английски")
    date_until_date = models.DateField(blank=True, null=True, verbose_name="Дата выдачи отсрочки")
    telegram_id = models.BigIntegerField(blank=True, null=True, verbose_name="Telegram id")

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"


class Session(models.Model):
    """
    Сеанс работы. За один сеанс может быть обработано множество писем.
    """
    time_begin = models.DateTimeField(null=False, editable=False, auto_now_add=True, verbose_name="Дата и время начала сессии")
    time_end = models.DateTimeField(null=True, verbose_name="Дата и время окончания сессии")
    log_file = models.CharField(null=True, max_length=4000, verbose_name="Путь к лог-файлу")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"


class Task(models.Model):
    """
    Задание (по сути это отдельно письмо которое обрабатывается)
    """
    time_begin = models.DateTimeField(null=False, editable=False, auto_now_add=True,
                                      verbose_name="Дата и время начала задания")
    time_end = models.DateTimeField(null=True, verbose_name="Дата и время окончания задания")
    task_from = models.CharField(null=True, max_length=254, verbose_name="От кого (email)")
    task_subject = models.CharField(null=True, max_length=2000, verbose_name="Тема (email)")
    task_body_type = models.CharField(null=True, max_length=4, verbose_name="Типа тела письма (TEXT;HTML;MIX)")
    task_body_html = models.TextField(null=True, verbose_name="Тело письма HTML")
    task_body_text = models.TextField(null=True, verbose_name="Тело письма TEXT")
    task_error = models.CharField(null=True, max_length=4000, verbose_name="Сообщение об ошибке")
    number_of_attempts = models.PositiveSmallIntegerField(null=True, verbose_name="Количество попыток")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task_from}-{self.task_subject}"

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Payment(models.Model):
    """
    Платёж
    """
    PAYMENT_PURPOSE_VOC = [
        ('ДШ', 'Друзья Школы'),
    ]
    PAYMENT_SYSTEM_VOC = [
        ('GC', 'GetCourse'),
        ('PK', 'PayKeeper'),
    ]
    name_of_service = models.CharField(null=True, max_length=255, verbose_name="Наименование услуги (как в письме)")
    payment_id = models.CharField(null=True, max_length=10, verbose_name="ID платежа (как в письме)")
    amount = models.PositiveSmallIntegerField(null=True, verbose_name="Сумма платежа")
    sales_slip = models.CharField(null=True, max_length=500, verbose_name="Кассовый чек 54-ФЗ (ссылка на него)")
    card_number = models.CharField(null=True, max_length=20, verbose_name="Номер кредитной карты плательщика")
    card_type = models.CharField(null=True, max_length=10, verbose_name="Тип кредитной карты плательщика")
    payment_purpose = models.CharField(
        max_length=2,
        choices=PAYMENT_PURPOSE_VOC,
        default='ДШ',
        verbose_name='Назначение платежа',
    )
    last_name = models.CharField(null=True, max_length=255, verbose_name="Фамилия по русски")
    first_name = models.CharField(null=True, max_length=255, verbose_name="Имя по русски")
    fio = models.CharField(db_index=True, null=True, max_length=500, verbose_name="Фамилия и Имя по русски")
    email = models.CharField(db_index=True, null=True, max_length=254, verbose_name="Email")
    telegram = models.CharField(db_index=True, null=True, max_length=32, verbose_name="Telegram name")
    time_create = models.DateTimeField(null=False, editable=False, auto_now_add=True, verbose_name="Дата создания")
    payment_system = models.CharField(
        max_length=2,
        choices=PAYMENT_SYSTEM_VOC,
        default='GC',
        verbose_name='Платёжная система',
    )
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fio} {self.payment_system} {self.payment_id}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

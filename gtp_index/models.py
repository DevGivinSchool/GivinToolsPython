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
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"


class Participant(models.Model):
    PARTICIPANT_TYPE_CHOICES = [
        ('N', 'новый участник (первый месяц)'),
        ('P', 'регулярный участник'),
        ('B', 'заблокированный'),
        ('E', 'наш сотрудник'),
        ('V', 'VIP (особые условия, например, участие без оплаты)'),
    ]
    last_name = models.CharField(null=True, max_length=2000, verbose_name="Фамилия по русски")
    first_name = models.CharField(null=True, max_length=2000, verbose_name="Имя по русски")
    fio = models.CharField(db_index=True, null=True, max_length=4000, verbose_name="Фамилия и Имя по русски")
    email = models.CharField(db_index=True, null=True, max_length=254, verbose_name="Email")
    telegram = models.CharField(db_index=True, null=True, max_length=32, verbose_name="Telegram name")
    time_begin = models.DateTimeField(editable=False, default=datetime.date.today, verbose_name="Дата создания")
    time_end = models.DateTimeField(null=True, verbose_name="Дата блокировки")
    login = models.CharField(null=True, max_length=2000,
                             verbose_name="Логин пользователя в домене @givinschool.org, соответствует почте")
    password = models.CharField(null=True, max_length=30, verbose_name="Пароль участника")
    payment_date = models.DateField(null=True, default=datetime.date.today, verbose_name="Дата оплаты")
    number_of_days = models.PositiveSmallIntegerField(null=True, verbose_name="Количество оплаченных дней")
    deadline = models.DateField(null=True, verbose_name="Дата следующей оплаты")
    comment = models.CharField(null=True, max_length=4000, verbose_name="Комментарий")
    until_date = models.DateField(null=True, verbose_name="Дата до которой отсрочен платёж")
    type = models.CharField(
        max_length=1,
        choices=PARTICIPANT_TYPE_CHOICES,
        default='N',
        verbose_name="Тип участника: P - регулярный участник; B - заблокированный; E - наш сотрудник; V - VIP (особые условия, например, участие без оплаты)",
    )
    last_name_eng = models.CharField(null=True, max_length=2000, verbose_name="Фамилия по английски")
    first_name_eng = models.CharField(null=True, max_length=2000, verbose_name="Имя по английски")
    fio_eng = models.CharField(db_index=True, null=True, max_length=4000, verbose_name="Фамилия и Имя по английски")
    date_until_date = models.DateField(null=True, verbose_name="Дата выдачи отсрочки")
    telegram_id = models.BigIntegerField(null=True, verbose_name="Telegram id")

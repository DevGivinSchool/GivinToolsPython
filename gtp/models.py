from django.db import models


class TeamMember(models.Model):
    """
    Участник команды
    """
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
    last_name_eng = models.CharField(blank=True, null=True, max_length=255, verbose_name="Фамилия по английски")
    first_name_eng = models.CharField(blank=True, null=True, max_length=255, verbose_name="Имя по английски")
    fio_eng = models.CharField(blank=True, db_index=True, null=True, max_length=500, verbose_name="Фамилия и Имя по английски")
    date_until_date = models.DateField(blank=True, null=True, verbose_name="Дата выдачи отсрочки")
    telegram_id = models.BigIntegerField(blank=True, null=True, verbose_name="Telegram id")

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Участник команды"
        verbose_name_plural = "Участники команды"

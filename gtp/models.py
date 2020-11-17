import datetime
from django.db import models


class TeamMember(models.Model):
    """
    Участник команды
    """
    MEMBER_SEX_VOC = [
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    ]
    last_name = models.CharField(blank=True, null=True, max_length=255, verbose_name="Фамилия по русски")
    first_name = models.CharField(blank=True, null=True, max_length=255, verbose_name="Имя по русски")
    last_name_eng = models.CharField(blank=True, null=True, max_length=255, verbose_name="Фамилия по английски")
    first_name_eng = models.CharField(blank=True, null=True, max_length=255, verbose_name="Имя по английски")
    email = models.CharField(blank=True, db_index=True, null=True, max_length=254, verbose_name="Email")
    telegram = models.CharField(blank=True, db_index=True, null=True, max_length=32, verbose_name="Telegram name")
    filial = models.CharField(blank=True, null=True, max_length=255, verbose_name="К какому филиалу относится")
    retrit = models.CharField(blank=True, null=True, max_length=255, verbose_name="С какого ретрита")
    birthday = models.DateField(blank=True, null=True, verbose_name="Дата выдачи отсрочки")
    sex = models.CharField(
        blank=True,
        null=True,
        max_length=1,
        choices=MEMBER_SEX_VOC,
        default='М',
        verbose_name="Пол: М - мужской; Ж - женский",
    )
    time_begin = models.DateTimeField(null=False, editable=False, auto_now_add=True, verbose_name="Дата создания")
    time_end = models.DateTimeField(blank=True, editable=False, null=True, verbose_name="Дата блокировки")
    login = models.CharField(blank=True, null=True, max_length=100,
                             verbose_name="Логин пользователя в домене @givinschool.org, соответствует почте")
    password = models.CharField(blank=True, null=True, max_length=32, verbose_name="Пароль участника")
    comment = models.CharField(blank=True, null=True, max_length=4000, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Участник команды"
        verbose_name_plural = "Участники команды"

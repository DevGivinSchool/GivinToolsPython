import datetime
from django.db import models


class Settings(models.Model):
    """
    Настройки приложения
    """
    key = models.CharField(null=False, max_length=255, verbose_name="Ключ")
    value = models.CharField(null=True, max_length=2000, verbose_name="Значение")
    type = models.CharField(null=True, max_length=255, verbose_name="Тип")
    inserted_date = models.DateTimeField(null=False, editable=False, auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(null=True, editable=False, auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"{self.key}={self.value}"

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"

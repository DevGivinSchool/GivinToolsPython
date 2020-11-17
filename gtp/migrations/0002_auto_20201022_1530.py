# Generated by Django 3.1 on 2020-10-22 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teammember',
            name='type',
        ),
        migrations.AddField(
            model_name='teammember',
            name='sex',
            field=models.CharField(blank=True, choices=[('М', 'Мужской'), ('Ж', 'Женский')], default='М', max_length=1, null=True, verbose_name='Пол: М - мужской; Ж - женский'),
        ),
    ]

# Generated by Django 3.1 on 2020-10-22 12:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('gtp_index', '0011_auto_20201021_1511'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='task',
        ),
        migrations.RemoveField(
            model_name='task',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='task',
            name='session',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Session',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
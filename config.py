# Параметры программы, использовать так:
# import config
# print config.config['param1']
import logging
import os

config = dict(
    # Логирование производится в папку где лежит скрипт/log
    log_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log'),
    log_level=logging.DEBUG,
    postgres_dbname='gs',
    postgres_host='172.26.12.29',
    postgres_port='5432'
)

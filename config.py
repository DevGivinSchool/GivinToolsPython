# Параметры программы, использовать так:
# import config
# print config.config['param1']
import os
import logging

config = dict(
    # Логирование производится в папку где лежит скрипт/log
    log_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log'),
    log_level=logging.DEBUG
)
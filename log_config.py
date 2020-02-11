import logging
import os

"""
Логирование может осуществляться независимо на каждом компьютере где запускаются скрипты, поэтому этот файл 
добавлен в gitignore. 

"""

# Логирование по умолчанию производится в папку где лежита скрипты/log
log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')
log_level = logging.INFO
# log_level = logging.DEBUG


import logging
import os
import PASSWORDS

"""
Логирование может осуществляться независимо на каждом компьютере где запускаются скрипты, поэтому этот файл 
добавлен в gitignore. 

"""

# Логирование по умолчанию производится в папку где лежита скрипты/log
log_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log')
prog_name = os.path.basename(os.path.realpath(__file__))
prog_name_without_ext = prog_name.split(".")[0]
if PASSWORDS.DEBUG:
    log_level = logging.DEBUG
else:
    log_level = logging.INFO


if __name__ == '__main__':
    print(log_dir)
    print(prog_name)
    print(prog_name_without_ext)
    print(log_level)

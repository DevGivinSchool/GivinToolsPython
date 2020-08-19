import logging
import os
import core.PASSWORDS as PASSWORDS
from datetime import datetime


def get_prog_name(file_path):
    """
    Процедура выделяет из полного пути имя файла с расширение и без
    :param file_path: Полный путь к файлу
    :return: Имя файла с расширение, имя файла без расширения
    """
    prog_name_ = os.path.basename(file_path)
    prog_name_without_ext_ = prog_name_.split(".")[0]
    extention_ = prog_name_.split(".")[1]
    return prog_name_, prog_name_without_ext_, extention_


def get_logger(program_file=None, log_file=None, dt=True):
    """
    Процедура создаёт logger на основе либо program_file либо log_file.
    Логирование по умолчанию производится в папку где лежит скрипт/log
    :param program_file: Полный путь к исполняемому файлу
    :param log_file: Полный путь к лог файлу
    :param dt: Включать ли в имя лог файла дату и время
    :return: logger
    """
    # Лог файл можно задать явно
    if log_file:
        log_dir = os.path.dirname(log_file)
        prog_name, prog_name_without_ext, extention = get_prog_name(log_file)
        log_name = prog_name
    else:
        # Если лог файл явно не задан, собираем его по частям
        if program_file:
            # Логирование по умолчанию производится в папку где лежит скрипт/log
            # т.к. теперь все скрипты переместились на уровень ниже, то логирование нужно выполнять на 1 уровень выше
            log_dir = os.path.join(os.path.dirname(os.path.dirname(program_file)), 'log')
            prog_name, prog_name_without_ext, extention = get_prog_name(program_file)
            extention = 'log'
            log_name = prog_name_without_ext
        else:
            raise Exception("ERROR: Нужно либо явно задать log_file либо передать program_file")
    if PASSWORDS.DEBUG:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    # Если директории для логирования не существует создаём её
    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except OSError:
            print(f"Creation of the directory {log_dir} failed")
            exit(1)
    log_file_ = ""
    try:
        if dt:
            now = "_" + datetime.now().strftime("%Y%m%d%H%M%S")
        else:
            now = ""
        log_file_ = os.path.join(log_dir, f"{log_name}{now}.{extention}")
    except OSError as err:
        print(f"Creation of the log_file from log_path:'{log_dir}', log_name:'{log_name}', "
              f"now:{now}, extention:{extention} failed")
        print(err)
        exit(1)
    # log_formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(process)d:%(thread)d - %(message)s')
    log_formatter = logging.Formatter('%(asctime)s|%(levelname)8s| %(message)s')
    handler = logging.FileHandler(log_file_, mode='w', encoding='utf-8')
    handler.setFormatter(log_formatter)
    custom_logger = logging.getLogger(prog_name_without_ext)
    custom_logger.setLevel(log_level)
    custom_logger.addHandler(handler)
    # print(custom_logger.handlers[0].baseFilename)
    return custom_logger

import transliterate
import re
import os
import time

abc = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k',
       'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v',
       'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z',
       'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
       'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
       'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'shh', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
       }


def translit_name(text):
    """
    Транслитерация строки
    :param text:
    :return:
    """
    text = text.replace("'", "").strip()
    text2 = ""
    for s in text:
        text2 += abc.get(s, "_")
    return text2
    # return transliterate.translit(text, reversed=True).replace("'", "").strip()


def is_eng(text):
    """
    Проверка что текст английский
    :param text:
    :return:
    """
    pattern_eng = re.compile("[A-Za-z]+")
    return pattern_eng.match(text.replace(' ', ''))


def is_rus(text):
    """
    Проверка что текст русский
    :param text:
    :return:
    """
    pattern_rus = re.compile("[А-Яа-я]+")
    return pattern_rus.match(text.replace(' ', ''))


def get_login(familia_, name_, type=None):
    """
    Создание логина из фамилии и имени. # У некоторых фамили и имена сложные = несколько слов через пробел,
    поэтому пробел заменяю на подчёркивание
    :param type: team - для команды; frend - КПД
    :param familia_:
    :param name_:
    :return: login_
    """
    if familia_ is None or familia_ == '':
        raise Exception('ERROR: Для логина обязательно нужна фамилия')
    familia_ = familia_.strip()
    if is_rus(familia_):
        familia_ = translit_name(familia_.lower()).replace(' ', '_')
    else:
        familia_ = familia_.lower().replace(' ', '_')
    if name_ is None or name_ == '':
        return familia_
    else:
        name_ = name_.strip()
        if is_rus(name_):
            name_ = translit_name(name_.lower()).replace(' ', '_')
        else:
            name_ = name_.lower().replace(' ', '_')
        if type == "team":
            return familia_ + "." + name_[0]
            # ivanov.i
        else:
            return familia_ + "_" + name_
            # ivanov_ivan


def split_str(line):
    """
    Разделяет строку через ';' и пробел, возвращает список
    :param line:
    :return:
    """
    line_ = line.split(';', maxsplit=1)
    # print(line_, len(line_))
    if len(line_) < 2:
        raise Exception(f"ERROR: Строка '{line_}' не разделяется через точку с запятой")
    # print(f"line_={line_}; line_[0]={line_[0]}; line_[1]={line_[1]}")
    return line_


def str_normalization1(text):
    """
    Нормализация строки = удалить все пробелы и привести к нижнему регистру
    :param text:
    :return:
    """
    return text.lower().replace(" ", "")


def str_normalization2(text):
    """
    Нормализация строки 2 = оставить только буквы, все остальные символы удаляются
    :param text:
    :return:
    """
    return ''.join(c for c in text if c.isalpha())


def delete_obsolete_files(path, days, logger):
    """
    Процедура удаления устаревших файлов (старше Х дней).
    :param path: Папка из которой удаляются файлы.
    :param days: Количество дней больше которого файлы считаются устаревшими.
    :param logger: логгер
    """
    logger.info("Процедура удаления устареших файлов")
    deadline = time.time() - (days * 86400)
    logger.debug(f"time.time()={time.time()}")
    logger.debug(f"interval={days * 86400}")
    logger.debug(f"deadline={deadline}")
    files = os.listdir(path)
    # file_path = os.path.join(get_file_directory(__file__), "logs/")
    for file in files:
        # logger.debug(f"обработка файла {file}")
        file = os.path.join(path, file)
        logger.debug(f"обработка файла {file}")
        if os.path.isfile(os.path.join(path, file)):
            change_time = os.stat(file).st_mtime
            # У старых файлов diff отрицательный
            logger.debug(f"time_creation={change_time}; diff={change_time - deadline}")
            if change_time < deadline:
                logger.info(f"delete {file}")
                os.remove(file)


if __name__ == '__main__':
    print(translit_name("бiлавина светлана"))
    print(get_login("бiлавина", "свiтлана", type=None))

import transliterate
import re


def translit_name(text):
    return transliterate.translit(text, reversed=True).replace("'", "").strip()


def is_eng(text):
    pattern_eng = re.compile("[A-Za-z]+")
    return pattern_eng.match(text.replace(' ', ''))


def is_rus(text):
    pattern_rus = re.compile("[А-Яа-я]+")
    return pattern_rus.match(text.replace(' ', ''))


def get_login(familia_, name_):
    """
    Создание логина из фамилии и имени. # У некоторых фамили и имена сложные = несколько слов через пробел,
    поэтому пробел заменяю на подчёркивание
    :param familia_:
    :param name_:
    :return: login_
    """
    if familia_ is None or familia_ == '':
        raise Exception('ERROR: Для логина обязательно нужна фамилия')
    familia_ = familia_.strip()
    if is_rus(familia_):
        familia_ = translit_name(familia_.lower()).replace(' ', '_')
    if name_ is None or name_ == '':
        return familia_
    else:
        name_ = name_.strip()
        if is_rus(name_):
            name_ = translit_name(name_.lower()).replace(' ', '_')
        return familia_ + "_" + name_


def split_str(line):
    """
    Разделяет строку через табуляцию и пробел, возвращает список
    :param line:
    :return:
    """
    line_ = line.split('\t', maxsplit=1)
    # print(line_, len(line_))
    if len(line_) < 2:
        line_ = line.split(' ', maxsplit=1)
        if len(line_) < 2:
            raise Exception(f"ERROR: Строка ФИО '{line_}' не разделяется ни через пробел ни через табуляцию")
    # print(f"line_={line_}; line_[0]={line_[0]}; line_[1]={line_[1]}")
    return line_

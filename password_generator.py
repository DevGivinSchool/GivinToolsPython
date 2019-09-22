import random
import string
import re


def random_password(strong=False, long=10, zoom=False):
    """
    Генератор паролей.
    :param zoom: Пароль для Zoom - два последних символа маленькие латениские буквы.
    :param strong: Пароль включает символы "@#$&".
    :param long: Длина паролья, для Zoom по умолчанию 10.
    :return: Словарь значений.
    """
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    if strong:
        chars = chars + "@#$&"
    password = ''.join(random.choice(chars) for _ in range(long))
    # Заменить все буквы которые могут быть
    # неправильно поняты пользователями
    for ch in ['l', 'j', 'i', '0', 'o', 'O']:
        if ch in password:
            password = password.replace(ch, random.choice(chars))
    # Пароль должен содержать хотя бы одну цифру (Zoom), если цифры нет, подставляем на третью позицию случайню цифру
    if not re.search(r'\d', password):
        password = password[:2] + random.choice(string.digits) + password[2 + 1:]
    # В сложном пароле должны быть и спецсимволы, если нет,
    # подставляем на третью позицию
    chars = set('@#$&', )
    if not any((c in chars) for c in password):
        password = password[:2] + random.choice(['@', '#', '$', '&']) + password[2 + 1:]
    # (Только для Zoom (zoom=True) Два последних символа - два маленькие буквы,
    # так удобнее потом дописывать 55
    if zoom:
        password = password[:-2] + random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
    return password

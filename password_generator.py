import random
import string
import re


def randompassword(strong=False, long=8):
    """Генератор пароля для Zoom"""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    if strong:
        chars = chars + "@#$&"
    password = ''.join(random.choice(chars) for x in range(long))
    # Заменить все буквы которые могут быть неправильно поняты пользователями
    for ch in ['l', 'j', 'i', '0', 'o', 'O']:
        if ch in password:
            password = password.replace(ch, random.choice(chars))
    # Пароль должен содержать хотя бы одну цифру (Zoom), если цифры нет, подставляем на третью позицию случайню цифру
    if not re.search(r'\d', password):
        password = password[:2] + random.choice(string.digits) + password[2 + 1:]
    # В сложном пароле должны быть и спецсимволы, если нет, подставляем на третью позицию
    chars = set('@#$&', )
    if not any((c in chars) for c in password):
        password = password[:2] + random.choice(['@', '#', '$', '&']) + password[2 + 1:]
    # (Только для Zoom (strong=False)) Два последних символа - два маленькие буквы, так удобнее потом дописывать 55
    if not strong:
        password = password[:-2] + random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
    return password

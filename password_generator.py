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
    # Набор символов пароля не должен содержать букв,
    # которые могут быть неправильно поняты пользователями
    # 'l', 'j', 'i', '0', 'o', 'O'
    ascii_uppercase_chars = ''.join(string.ascii_uppercase.split("O"))
    print(f"ascii_uppercase_chars={ascii_uppercase_chars}")
    digits_chars = string.digits.replace("0", random.choice(string.digits[1:]))
    temp_chars = ascii_uppercase_chars + digits_chars
    print(f"digits_chars={digits_chars}")
    ascii_lowercase_chars = string.ascii_lowercase \
        .replace("l", "") \
        .replace("j", "") \
        .replace("i", "") \
        .replace("o", "")
    print(f"ascii_lowercase_chars={ascii_lowercase_chars}")
    letters = ascii_uppercase_chars + digits_chars + ascii_lowercase_chars
    print(f"letters={letters}")
    chars = ascii_uppercase_chars + digits_chars + ascii_lowercase_chars
    print(f"chars1={chars}")
    if strong:
        chars = chars + "@#$&"
    print(f"chars2={chars}")
    if zoom:
        # Для zoom в самом конце пароля добавляются две маленькие буквы для удобства,
        # поэтому генерим его значально короче на 2 буквы
        long = long - 2
    password = ''.join(random.choice(chars) for _ in range(long))
    print(f"password 0={password}")
    # Пароль должен начинаться с буквы
    if not password[0].isalpha():
        password = random.choice(letters) + password[1:]
    print(f"password 1={password}")
    # Пароль должен содержать хотя бы одну цифру (Zoom), если цифры нет, подставляем на третью позицию случайню цифру
    if not re.search(r'\d', password):
        print(f"цифр нет")
        password = password[:2] + random.choice(digits_chars) + password[2:]
        password = adjust_password_length(password)
    print(f"password 2={password}")
    # В сложном пароле должны быть и спецсимволы, если нет, подставляем на четвёртую позицию
    chars = set('@#$&', )
    if not any((c in chars) for c in password):
        print(f"спецсимволов нет")
        password = password[:3] + random.choice(['@', '#', '$', '&']) + password[3:]
        password = adjust_password_length(password)
    print(f"password 3={password}")
    # (Только для Zoom (zoom=True) Два последних символа - два маленькие буквы,
    # так визуально удобнее потом дописывать 55
    if zoom:
        print(f"пароль для zoom")
        password = password + random.choice(ascii_lowercase_chars) + random.choice(ascii_lowercase_chars)
    print(f"password 4={password}")
    return password


def adjust_password_length(pswd):
    """
    Выкидываем из пароля начиная с 1 символа (0 всегда должна быть буква) первую попавшуюся букву,
    за счёт этого длина пароля при добавлении цифры или спецсимвола не увеличивается,
    и цифры\спецсимволы не затираются.
    :param pswd: Пароль на входе
    :return: Нормализованный пароль
    """
    seq = range(1, len(pswd), 1)
    for i in seq:
        if pswd[i].isalpha():
            # print(pswd[0:i] + pswd[i + 1:])
            return pswd[0:i] + pswd[i + 1:]



if __name__ == "__main__":
    print(random_password(strong=True, zoom=True))  # для ДШ
    # adjust_password_length('xpt4LkWS')

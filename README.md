# GivinToolsPython
Utilities for Givin School

Все утилиты имеют префикс gtp_ остальные файлы вспомогательные.

# ENV + PIP
-- Глобальная установка virtualenv
c:\> pip install virtualenv
-- Далее установка в проекте
-- Создание виртуального окружения
c:\> cd c:\mygit\GivinToolsPython
c:\MyGit\GivinToolsPython> python -m venv venv
-- Активация виртуального окружения
c:\MyGit\GivinToolsPython> cd c:\MyGit\GivinToolsPython\venv\Scripts\
c:\MyGit\GivinToolsPython\venv\Scripts> activate
-- Установка в виртуальное окружение всех необходимых зависимостей
c:\MyGit\GivinToolsPython\venv\Scripts> pip install -r c:\MyGit\GivinToolsPython\requirements.txt
-- Обновление самого pip в этом виртуальном окружении
c:\MyGit\GivinToolsPython\venv\Scripts> python -m pip install --upgrade pip

Далее настройка в PyCharm Project Interpreter

# GTP Mail

gtp_mail.py - Программа для работы с корпоративной почтой

# GTP Attendance Book

gtp_attendance_book.py - Программа отмечания посещаемости различных занятий в Zoom

# GTP Zoom

gtp_zoomus.py - Программа для работы с Zoom

# Первоначальные настройки сервера
# Linux

Создать отдельную поддиректорию в /var/log/ и дать на неё права учётной записи из под которой работает скрипт.
`mkdir /var/log/foo
chown userfoo /var/log/foo
chmod 600 /var/log/foo`

# Кодировки
Тело письма (body) кодируется как
Content-Type: text/plain; charset="windows-1251"
Content-Transfer-Encoding: quoted-printable
=C8=E2=E0=ED=EE=E2 =C8=E2=E0=ED

Если выполлнить декодирование
body2 = email_message.get_payload(decode=True)
тогда это все переводиться в 
body2=b'\xc8\xe2\xe0\xed\xee\xe2 \xc8\xe2\xe0\xed\r\n\xcf\xe5\xf2\xf0\xee\xe2 \xcf\xb8\xf2\xf0\r\n\xc0\xea\xf3\xeb\xe8\xed\xe0 \xc8\xe7\xf0\xe0\xeb\xfa\xe5\xe2\xed\xe0\r\n\r\n\r\n\r\n\r\n'

# Полезные команды 

pip freeze > c:\MyGit\GivinToolsPython\requirements.txt
pip install -r c:\MyGit\GivinToolsPython\requirements.txt

# Модули
IMAPClient:
    Github - https://github.com/mjs/imapclient
    Doc - https://imapclient.readthedocs.io/en/2.1.0/
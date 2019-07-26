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


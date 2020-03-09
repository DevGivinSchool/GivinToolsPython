# GivinToolsPython (GTP)
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

В случае ошибок лучше сначала попробовать установить все через PyCharm.

Если будет ошибка:
Error: pg_config executable not found.
нужно установить Postgres и добавить в PATH путь до pg_config

Если при установке Postgres на Windows возникает ошибка:
Unable to write inside TEMP environment variable path
http://igordcard.blogspot.com/2012/03/unable-to-write-inside-temp-environment.html
http://1stopit.blogspot.com/2011/01/postgresql-83-and-84-fails-to-install.html

Если возникла ошибка при установке lxml:
error xslt-config make sure the development packages of libxml2 and libxslt are installed
Бинарники lxml можно скачать с - https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

Если при установке psycopg2 возникает ошибка:
psycopgmodule.obj : error LNK2001: unresolved external symbol
Бинарники lxml можно скачать с - https://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg

Если pip не обновляется с ошибкой:
pip install -U pip==19.3.1

Если потом при запуске скрипта начинаются какие-то ошибки:
pip uninstall <package>
pip install <package>

# Проблемы с Chromedriver
Не смотря на то что драйвер в system32, python его в упор не видит
Ошибка: selenium.common.exceptions.WebDriverException: Message: 'chromedriver.exe' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home

Вот так можно установить последнюю версию драйвера
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

# Модули
IMAPClient:
    Github - https://github.com/mjs/imapclient
    Doc - https://imapclient.readthedocs.io/en/2.1.0/
    
# Backup Postgresql
Скрипты в папке backup (взял отсюда - https://wiki.postgresql.org/wiki/Automated_Backup_on_Linux)
# GivinToolsPython (GTP)
# Utilities for Givin School

Все исполняемые утилиты имеют префикс gtp_ (ШГ) или sf_ (ДШ).  

# Программы для Школы Гивина (gtp_)
**gtp_create_logins.py** - Создание различных логинов ШГ.  
**gtp_mark_event_attendance.py** - Программа отмечания посещаемости различных занятий в Zoom.  
**gtp_telegram_bot.py** - Телеграм бот для ШГ.  

# Программы для проекта Друзья Школы (ДШ)(sf_)
**sf.py** - Основная программа. Почтовый робот ДШ. Парсит почтовые оповещения об оплате, отмечает оплаты в БД, создаёт учётные записи yandex mail, zoom, отправляет почтовые оповещения email, telegram. 
**sf_daily_works.py** - Различные ежедневные отчёты.  
**sf_participant_block.py** - Блокировка участника. Можно блокировать участников в ручном режиме по списку.  
**sf_participant_create.py** - Создание участника. Можно создавать участников в ручном режиме по списку.  
**sf_telegram_bot.py** - Телеграм бот для ДШ.  

# Структура папок проекта
**arch\\** - Архивные материалы, которые жалко выбрасывать.  
**backup\\** - Скрипты резервного копирования БД Postgres (взято отсюда - https://wiki.postgresql.org/wiki/Automated_Backup_on_Linux)  
**db_scripts\\** - SQL скрипты.  
**log\\** - Папка для логов (в проекте не присутсвует, т.к. создаётся в процесса выполнения).  
**stuff\\** - Вспомогательные материалы.  
&nbsp;  &nbsp;  |- backup.cmd - Архивировать папку проекта.  
&nbsp;  &nbsp;  |- compare_two_lists.py - Сравнение двух list.  
&nbsp;  &nbsp;  |- create_inserts.py - Для ДШ. Создание insert-s по CSV файлу.  
&nbsp;  &nbsp;  |- install_chromedriver.py - Установка chromedriver.  
&nbsp;  &nbsp;  |- yandex_connect_token_get_by_code.py - Получение токена для Яндекс приложения.  
&nbsp;  &nbsp;  |- zoom_connect_logins.py - Работа с zoom в браузере с помощью selenium.  
**test\\** - Испытание различных возможностей и тесты.  

# Полезные материалы

## Команды
```
python manage.py runserver
python manage.py makemigrations  
python manage.py migrate  
python manage.py makemigrations --name migration_name app_name --empty  
```
### Миграция 
```
INSERT INTO gtp_teammember (id, last_name, first_name, telegram, email, password, filial, retrit, comment, time_begin, time_end, birthday) select id, last_name, first_name, telegram, email, password, filial, retrit, comment, time_begin, time_end, birthday FROM team_members ;
```
Установить последовательности на максимальное ID - https://wiki.postgresql.org/wiki/Fixing_Sequences

## Установка зависимостей  
`pip freeze > c:\MyGit\GivinToolsPython\requirements.txt`  
`pip install -r c:\MyGit\GivinToolsPython\requirements.txt`  
В случае ошибок лучше сначала попробовать установить все через PyCharm.  

## ENV + PIP. Создание виртуального окружения.
-- Глобальная установка virtualenv  
`c:\> pip install virtualenv`  
-- Далее установка в проекте  
-- Создание виртуального окружения  
`c:\> cd c:\mygit\GivinToolsPython`  
`c:\MyGit\GivinToolsPython> python -m venv venv`  
-- Активация виртуального окружения  
`c:\MyGit\GivinToolsPython> cd c:\MyGit\GivinToolsPython\venv\Scripts\`  
`c:\MyGit\GivinToolsPython\venv\Scripts> activate`  
-- Обновление самого pip в этом виртуальном окружении  
`c:\MyGit\GivinToolsPython\venv\Scripts> python -m pip install --upgrade pip`  
-- Установка в виртуальное окружение всех необходимых зависимостей  
`c:\MyGit\GivinToolsPython\venv\Scripts> pip install -r c:\MyGit\GivinToolsPython\requirements.txt`  
Далее настройка в PyCharm Project Interpreter 

## Кодировки в email
Тело письма (body) кодируется как
Content-Type: text/plain; charset="windows-1251"
Content-Transfer-Encoding: quoted-printable
=C8=E2=E0=ED=EE=E2 =C8=E2=E0=ED

Если выполлнить декодирование
body2 = email_message.get_payload(decode=True)
тогда это все переводиться в 
body2=b'\xc8\xe2\xe0\xed\xee\xe2 \xc8\xe2\xe0\xed\r\n\xcf\xe5\xf2\xf0\xee\xe2 \xcf\xb8\xf2\xf0\r\n\xc0\xea\xf3\xeb\xe8\xed\xe0 \xc8\xe7\xf0\xe0\xeb\xfa\xe5\xe2\xed\xe0\r\n\r\n\r\n\r\n\r\n'

## Различные проблемы при установке зависимостей 
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
`pip install -U pip==19.3.1`  

Если потом при запуске скрипта начинаются какие-то ошибки:  
`pip uninstall <package>`  
`pip install <package>`  

## Проблемы с Chromedriver
Не смотря на то что драйвер в system32, python его в упор не видит  
Ошибка: selenium.common.exceptions.WebDriverException: Message: 'chromedriver.exe' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home  
** ./stuff/install_chromedriver.py **  
Вот так можно установить последнюю версию драйвера  
```
from selenium import webdriver  
from webdriver_manager.chrome import ChromeDriverManager  
driver = webdriver.Chrome(ChromeDriverManager().install())  
```
## Модули используемые в проекте
**IMAPClient**  

&nbsp;  &nbsp;  Github - https://github.com/mjs/imapclient  
&nbsp;  &nbsp;  Doc - https://imapclient.readthedocs.io/en/2.1.0/  

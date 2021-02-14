-- ===============================================================
-- Поиск участника
select
*
--id, last_name, first_name, fio, email, telegram, time_begin, time_end, login, password, payment_date, number_of_days, deadline, regexp_replace(comment, E'[\n\r]+', ' ', 'g' ), until_date, type
from public.participants
where
--telegram=lower('ххххх')
--last_name like upper('%ххххх%')
--last_name_eng like upper('%ххххх%')
id=1234
;

-- ===============================================================
-- Список платежей конкретного участника
select
*
--id, last_name, first_name, fio, email, telegram, time_begin, time_end, login, password, payment_date, number_of_days, deadline, regexp_replace(comment, E'[\n\r]+', ' ', 'g' ), until_date, type
from public.payments
where
--telegram=lower('ххххх')
--last_name like upper('%ххххх%')
--last_name_eng like upper('%ххххх%')
participant_id=1234
order by id
;

-- ===============================================================
-- Обновить участника
update participants set
email=lower('@')
,telegram=lower('@')
where
--telegram=lower('ххххх')
--last_name like upper('%ххххх%')
--last_name_eng like upper('%ххххх%')
id=1234
;

-- ===============================================================
-- Проставить дату оплаты
update participants set
payment_date=to_date('18.10.2019', 'DD.MM.YYYY'),
--payment_date=NOW(),
number_of_days=30,
deadline=to_date('18.10.2019', 'DD.MM.YYYY')+interval '1' day * 30,
--deadline=NOW()+interval '1' day * 30,
comment=NULL, type='P', until_date=null
where
--telegram=lower('ххххх')
--last_name like upper('%ххххх%')
--last_name_eng like upper('%ххххх%')
id=1234
;

-- ===============================================================
-- Получение списка должников
select
--deadline, until_date,
--CURRENT_TIMESTAMP,
--deadline - CURRENT_TIMESTAMP as "INTERVAL",
--until_date - CURRENT_TIMESTAMP as "INTERVAL2",
id, type,
last_name as "Фамилия", first_name as "Имя", email, telegram,
payment_date "Дата оплаты", number_of_days as "Дней", deadline "Оплачено до",
until_date as "Отсрочка до", regexp_replace(comment, E'[\n\r]+', ' ', 'g' )
FROM public.participants
where type in ('P', 'N')
--and number_of_days <> 45
and ((deadline - CURRENT_TIMESTAMP < interval '0 days' and until_date is null)
or (until_date - CURRENT_TIMESTAMP < interval '0 days' and until_date is not null))
order by last_name;

-- ===============================================================
-- Удаление участника
----select * from payments where participant_id=xxxx;
----update payments set participant_id=xxxx where participant_id=xxxx;
----select * from participants where id=xxxx;
----delete from participants where id=xxxx;

-- ===============================================================
-- Удаление task чтобы обойти - ВНИМАНИЕ: Это письмо уже обрабатывалось!
----select count(*) from tasks;
----select * from tasks where task_uuid=1021;
----delete from tasks where task_uuid=1014;

-- ===============================================================
-- Проверка неправильности периода оплаты и исправление этой ситуации
SELECT
id, type,
last_name as "Фамилия", first_name as "Имя",
payment_date "Дата оплаты", number_of_days as "Дней", deadline "Оплачено до", payment_date+interval '1' day * 30
FROM public.participants
WHERE type in ('P', 'N') and sf_level=1
order by last_name

update public.participants set deadline = payment_date+interval '1' day * 30
WHERE type in ('P', 'N') and sf_level=1 and payment_date+interval '1' day * 30 <> deadline

-- ===============================================================
-- Создать участника
insert into public.participants(
	last_name, first_name, fio, last_name_eng, first_name_eng, fio_eng, email, telegram, login, password, payment_date, number_of_days, deadline, type, comment)
	VALUES (
	upper('last_name'),
	upper('first_name'),
	upper('fio'),
	upper('last_name_eng'),
	upper('first_name_eng'),
	upper('fio_eng'),
	lower('email'),
	lower('telegram'),
	'login',
	'password',
	to_date('18.02.2020', 'dd.mm.yyyy'),
	30,
	--to_date('01.03.2020', 'dd.mm.yyyy') + INTERVAL '30 day',
	to_date('01.03.2020', 'dd.mm.yyyy'),
	'N',
	'' -- comment
	);
-- ===============================================================
--Получение списка участников (как регулярных так и заблокированных)
select id, last_name, first_name, fio, email, telegram, login, password, payment_date, number_of_days, deadline, until_date, regexp_replace(comment, E'[\\n\\r]+', ' ', 'g' )
	FROM public.participants
	where type in ('P', 'N')
	--where type='B'
order by last_name;

-- ===============================================================
-- Кто сегодня оплатил
select * from participants where payment_date=to_date('05.10.2019', 'dd.mm.yyyy');

-- Получение списка новичков
select
--deadline, until_date,
--CURRENT_TIMESTAMP,
--deadline - CURRENT_TIMESTAMP as "INTERVAL",
--until_date - CURRENT_TIMESTAMP as "INTERVAL2",
id, type,
last_name as "Фамилия", first_name as "Имя", email, telegram,
payment_date "Дата оплаты", number_of_days as "Дней", deadline "Оплачено до",
until_date as "Отсрочка до", regexp_replace(comment, E'[\n\r]+', ' ', 'g' )
FROM public.participants
where type in ('N')
--and number_of_days <> 45
and CURRENT_TIMESTAMP - payment_date < interval '3 days'
order by last_name;

-- ===============================================================
-- Нормализация БД
update public.participants
	set last_name=trim(upper(last_name)), first_name=trim(upper(first_name)),
	    fio=trim(upper(fio)), email=trim(lower(email)),
	    telegram=trim(lower(telegram)), login=trim(lower(login)),
	    last_name_eng=trim(upper(last_name_eng)), first_name_eng=trim(upper(first_name_eng)),
	    fio_eng=trim(upper(fio_eng))

-- ===============================================================
-- Выявление дублей участников
--delete from participants where id in (
select
--p.id
--p.*
p.id, p.last_name, p.first_name, p.type
from participants as "p",
(select last_name, first_name, count(last_name) as "ct"
from participants
group by last_name, first_name
having count(last_name)>1
order by last_name) as "tab1"
where
p.last_name = tab1.last_name and p.first_name=tab1.first_name
and p.type='B'
order by p.last_name
--)
;

-- Удаление дублей которые TYPE='B'
delete from participants where id in (
select
p.id
--p.*
--p.id, p.last_name, p.first_name, p.type
from participants as "p",
(select last_name, first_name, count(last_name) as "ct"
from participants
group by last_name, first_name
having count(last_name)>1
order by last_name) as "tab1"
where
p.last_name = tab1.last_name and p.first_name=tab1.first_name
and p.type='B'
order by p.last_name
)
;

-- ===============================================================
-- Windows

-- BACKUP
pg_dump.exe -U postgres -d gs -f d:\YandexDisk\TEMP\gs20190908.sql
pg_dump gs > gs20190920.sql
-- Вариант с паролем смотри в PASSWORDS.py
SET PGPASSWORD=<PassWord>
"C:\Program Files (x86)\pgAdmin 4\v4\runtime\pg_dump.exe" --file "D:\YandexDisk\TEMP\GS\20191023.sql" --host "<ip>" --port "5432" --username "postgres" --no-password --verbose --format=p --encoding "UTF8" "gs"
-- RESTORE
cd "c:\Program Files\PostgreSQL\11\bin"
psql.exe -U postgres -d gs -f d:\YandexDisk\TEMP\gs20190906.sql

-- ===============================================================

-- Clear scheme
DO $$
begin
    TRUNCATE sessions_tasks;
	TRUNCATE task_steps;
	TRUNCATE payments;
	commit;
	TRUNCATE tasks CASCADE;
	TRUNCATE sessions CASCADE;
	commit;
end $$;

-- ===============================================================
-- Список команды
SELECT id, last_name, first_name, telegram, birthday FROM public.team_members where id<>1 order by last_name;

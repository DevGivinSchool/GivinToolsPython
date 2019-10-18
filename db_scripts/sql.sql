-- Создать пользователя
INSERT INTO public.participants(
	last_name, first_name, fio, email, telegram, login, password, payment_date, number_of_days, deadline, type)
	VALUES (upper('МАССОЛЬД'), upper('МАРИНА'), upper('МАССОЛЬД МАРИНА'), lower('mmassold@gmx.de'), lower('@marinamassold1975'), 'massold_marina@givinschool.org', 'rkP&Q8Sxfq', to_date('15.10.2019', 'dd.mm.yyyy'), 30, to_date('15.10.2019', 'dd.mm.yyyy') + INTERVAL '30 day', 'N');

-- Обновить пользователя
UPDATE participants SET
email=lower('@')
,telegram=lower('@')
where
--telegram=lower('@')
--last_name=upper('СМИРНОВ')
id=1294
;

-- Добавить дней пользователю
UPDATE participants SET
payment_date = to_date('10.10.2019', 'dd.mm.yyyy'),
number_of_days = 97,
deadline = to_date('10.10.2019', 'dd.mm.yyyy') + INTERVAL '97 day'
where
--telegram=lower('@M505058')
last_name=upper('фридман')
;



-- Блокировка участника (= ПОМЕНЯТЬ ПАРОЛЬ ZOOM)
UPDATE participants SET type='B', password=password||'55'
where
--telegram=lower('@M505058')
last_name=upper('Абдуллаева')
;

-- ===============================================================
-- Поиск участника
SELECT
*
--id, last_name, first_name, fio, email, telegram, time_begin, time_end, login, password, payment_date, number_of_days, deadline, comment, until_date, type
FROM public.participants
where
--telegram=lower('@')
--last_name=upper('СМИРНОВ')
id=1294
;

-- ===============================================================
--Получение списка участников (как регулярных так и заблокированных)
SELECT id, last_name, first_name, fio, email, telegram, login, password, payment_date, number_of_days, deadline, until_date, comment
	FROM public.participants
	where type='P'
	--where type='B'
order by last_name;

-- ===============================================================
-- Получение списка должников
SELECT
--deadline, until_date,
--CURRENT_TIMESTAMP,
--deadline - CURRENT_TIMESTAMP as "INTERVAL",
--until_date - CURRENT_TIMESTAMP as "INTERVAL2",
last_name as "Фамилия", first_name as "Имя", email, telegram,
payment_date "Дата оплаты", number_of_days as "Дней", deadline "Оплачено до",
until_date as "Отсрочка до", comment
FROM public.participants
WHERE type = 'P'
--and number_of_days <> 45
and ((deadline - CURRENT_TIMESTAMP < INTERVAL '0 days' and until_date is NULL)
or (until_date - CURRENT_TIMESTAMP < INTERVAL '0 days' and until_date is not NULL))
order by last_name;

-- ===============================================================
-- Проставить дату оплаты
--select * from participants where fio='ЛАНДЕНОК АННА';
--UPDATE participants SET payment_date=NOW(), number_of_days=30, deadline=NOW()+interval '1' day * number_of_days, comment=NULL, type='P' WHERE id=XXX;
--UPDATE participants SET payment_date=to_date('04.10.2019', 'DD.MM.YYYY'), number_of_days=30, deadline=to_date('04.10.2019', 'DD.MM.YYYY')+interval '1' day * number_of_days, comment=NULL, type='P' WHERE id=XXX;
--commit;
--select * from participants where fio='ЛАНДЕНОК АННА';

-- ===============================================================
-- Кто сегодня оплатил
select * from participants where payment_date=to_date('05.10.2019', 'dd.mm.yyyy');

-- ===============================================================
-- Нормализация БД
UPDATE public.participants
	SET last_name=trim(upper(last_name)), first_name=trim(upper(first_name)),
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
(SELECT last_name, first_name, count(last_name) as "ct"
FROM participants
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
(SELECT last_name, first_name, count(last_name) as "ct"
FROM participants
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
-- RESTORE
cd "c:\Program Files\PostgreSQL\11\bin"
psql.exe -U postgres -d gs -f d:\YandexDisk\TEMP\gs20190906.sql

-- ===============================================================

-- Clear scheme
DO $$
BEGIN
    TRUNCATE sessions_tasks;
	TRUNCATE task_steps;
	TRUNCATE payments;
	commit;
	TRUNCATE tasks CASCADE;
	TRUNCATE sessions CASCADE;
	commit;
END $$;

-- ===============================================================

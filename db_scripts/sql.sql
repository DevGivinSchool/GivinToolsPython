-- Получение списка должников
SELECT
last_name as "Фамилия", first_name as "Имя", email, telegram, 
payment_date "Дата оплаты", number_of_days as "Дней", deadline "Оплачено до", until_date as "Отсрочка до", comment
FROM public.participants
WHERE deadline - CURRENT_TIMESTAMP < INTERVAL '0 days'
      and isblocked = false
order by last_name;

-- ===============================================================
-- Проставить дату оплаты
--select * from participants where fio='КИСЕЛЕВ МИХАИЛ';
--UPDATE participants SET payment_date=NOW(), number_of_days=30, deadline=payment_date+number_of_days, comment=NULL, isblocked=false WHERE id=xxx;
--UPDATE participants SET payment_date=to_date('25.09.2019', 'DD.MM.YYYY'), number_of_days=30, deadline=payment_date+number_of_days, comment=NULL, isblocked=false WHERE id=xxx;
--commit;

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


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

-- ====================================
-- Windows

-- BACKUP
pg_dump.exe -U postgres -d gs -f d:\YandexDisk\TEMP\gs20190908.sql

-- RESTORE
cd "c:\Program Files\PostgreSQL\11\bin"
psql.exe -U postgres -d gs -f d:\YandexDisk\TEMP\gs20190906.sql
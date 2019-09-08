-- CentOS 7
-- Database: gs

-- DROP DATABASE gs;

CREATE DATABASE gs
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- ====================================
-- Ubuntu 16.4.6
-- Database: gs

-- DROP DATABASE gs;

CREATE DATABASE gs
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.utf8'
    LC_CTYPE = 'ru_RU.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- ====================================
-- Windows
-- Database: gs

-- DROP DATABASE gs;

CREATE DATABASE gs
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

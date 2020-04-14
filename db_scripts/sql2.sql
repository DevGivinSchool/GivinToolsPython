-- SQL запросы для отмечания посещаемости в zoom

-- ВАРИАНТ 1: столбец типа integer
ALTER TABLE public.zoom_table DROP COLUMN D1204_1;
ALTER TABLE public.zoom_table ADD COLUMN D1204_1 integer;

SELECT id, last_name, first_name, d1204_1, d1204_2, d1304_1, d1304_2, d1304_3, d1404_1
FROM public.zoom_table where id<>1 order by last_name;

-- ВАРИАНТ 2: столбец типа varchar
ALTER TABLE public.zoom_table DROP COLUMN D1204_1;
ALTER TABLE public.zoom_table ADD COLUMN D1204_1 character varying(1) COLLATE pg_catalog."default";

SELECT id, last_name, first_name,
coalesce(d1204_1, ''),
coalesce(d1204_2, '')
FROM public.zoom_table where id<>1 order by last_name;

-- Список команды
select id, last_name, first_name from team_members where id<>1 order by last_name;

-- Создать члена команды => ЕГО ЖЕ НУЖНО ВСТАВЛЯТЬ В ZOOM_TABLE!!!
INSERT INTO public.team_members(last_name, first_name, type)
	VALUES ('КИСЕЛЕВА', 'ЕЛЕНА', 1);
INSERT INTO public.zoom_table(last_name, first_name, type)
	VALUES ('КИСЕЛЕВА', 'ЕЛЕНА', 1);


-- Чистка таблицы отчёта
    update zoom_table set d1204_1=null;
    update zoom_table set d1204_2=null;

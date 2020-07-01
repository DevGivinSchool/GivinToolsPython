-- SQL запросы для отмечания посещаемости в zoom



-- ВАРИАНТ 1: столбец типа integer
ALTER TABLE public.zoom_table DROP COLUMN D1204_1;
ALTER TABLE public.zoom_table ADD COLUMN D1204_1 integer;

SELECT id,type,sort,last_name,first_name,_1204_1,_1204_2,_1304_1,_1304_2,_1304_3,_1404_1,_1404_2,_1404_3,_1504_1,_1504_2,_1504_3,_1604_1,_1604_2,_1704_1,_1704_2,_1704_3,_1804_1,_1804_2,_1804_3,_1904_1,_1904_2,_1904_3,_2004_1 FROM public.zoom_table where type=1
union all
SELECT id,type,sort,last_name,first_name,_1204_1,_1204_2,_1304_1,_1304_2,_1304_3,_1404_1,_1404_2,_1404_3,_1504_1,_1504_2,_1504_3,_1604_1,_1604_2,_1704_1,_1704_2,_1704_3,_1804_1,_1804_2,_1804_3,_1904_1,_1904_2,_1904_3,_2004_1 FROM public.zoom_table where type=2
union all
SELECT id,type,sort,last_name,first_name,_1204_1,_1204_2,_1304_1,_1304_2,_1304_3,_1404_1,_1404_2,_1404_3,_1504_1,_1504_2,_1504_3,_1604_1,_1604_2,_1704_1,_1704_2,_1704_3,_1804_1,_1804_2,_1804_3,_1904_1,_1904_2,_1904_3,_2004_1 FROM public.zoom_table where type=3
order by type, sort, last_name

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

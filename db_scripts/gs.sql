--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5 (Ubuntu 11.5-1.pgdg16.04+1)
-- Dumped by pg_dump version 11.5 (Ubuntu 11.5-1.pgdg16.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: participants_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participants_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participants_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participants (
    id integer DEFAULT nextval('public.participants_id_seq'::regclass) NOT NULL,
    last_name character varying(2000),
    first_name character varying(2000),
    fio character varying(4000),
    email character varying(254),
    telegram character varying(32),
    time_begin timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    time_end timestamp with time zone,
    login character varying(2000),
    password character varying(30),
    payment_date date DEFAULT CURRENT_DATE,
    number_of_days integer,
    deadline date,
    comment character varying(4000),
    until_date timestamp with time zone,
    isblocked boolean DEFAULT false NOT NULL
);


ALTER TABLE public.participants OWNER TO postgres;

--
-- Name: TABLE participants; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.participants IS 'Участники (участники различных мероприятий).';


--
-- Name: COLUMN participants.login; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participants.login IS 'Логин пользователя в домене @givinschool.org, соответствует почте.';


--
-- Name: COLUMN participants.password; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participants.password IS 'Пароль участника.';


--
-- Name: COLUMN participants.payment_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participants.payment_date IS 'Дата оплаты.';


--
-- Name: COLUMN participants.number_of_days; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participants.number_of_days IS 'Количество оплаченных дней. ';


--
-- Name: COLUMN participants.deadline; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participants.deadline IS 'Дата следующей оплаты.';


--
-- Name: COLUMN participants.comment; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participants.comment IS 'Комментарий.';


--
-- Name: COLUMN participants.until_date; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participants.until_date IS 'Дата до которой отсрочен платёж.';


--
-- Name: COLUMN participants.isblocked; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.participants.isblocked IS 'Участник заблокирован?';


--
-- Name: payment_purposes_voc; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_purposes_voc (
    id integer NOT NULL,
    name character varying(2000) NOT NULL,
    short_name character varying(2000) NOT NULL
);


ALTER TABLE public.payment_purposes_voc OWNER TO postgres;

--
-- Name: TABLE payment_purposes_voc; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.payment_purposes_voc IS 'Справочник назначений платежей (Друзья Школы, ПТО, ОК и т.п.) ';


--
-- Name: COLUMN payment_purposes_voc.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payment_purposes_voc.name IS 'Наименование типа платежа.';


--
-- Name: COLUMN payment_purposes_voc.short_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payment_purposes_voc.short_name IS 'Сокращённое наименование типа платежа.';


--
-- Name: payment_systems_voc; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_systems_voc (
    id integer NOT NULL,
    name character varying(2000),
    short_name character varying(2000)
);


ALTER TABLE public.payment_systems_voc OWNER TO postgres;

--
-- Name: TABLE payment_systems_voc; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.payment_systems_voc IS 'Справочник платёжных систем (GetCourse, PayKeeper и т.п.)';


--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payments_id_seq OWNER TO postgres;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    task_uuid integer NOT NULL,
    name_of_service character varying(2000),
    payment_id character varying(2000),
    amount integer,
    sales_slip character varying(2000),
    card_number character varying(2000),
    card_type character varying(2000),
    id integer DEFAULT nextval('public.payments_id_seq'::regclass) NOT NULL,
    payment_purpose integer NOT NULL,
    last_name character varying(2000),
    first_name character varying(2000),
    fio character varying(4000),
    email character varying(254),
    telegram character varying(32),
    participant_id integer,
    time_create timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    payment_system integer NOT NULL
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: COLUMN payments.task_uuid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.task_uuid IS 'Уникальное UUID задачи(письма) в котором был этот платёж.';


--
-- Name: COLUMN payments.name_of_service; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.name_of_service IS 'Наименование услуги (как в письме).';


--
-- Name: COLUMN payments.payment_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.payment_id IS 'ID платежа (как в письме).';


--
-- Name: COLUMN payments.amount; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.amount IS 'Сумма платежа.';


--
-- Name: COLUMN payments.sales_slip; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.sales_slip IS 'Кассовый чек 54-ФЗ (ссылка на него).';


--
-- Name: COLUMN payments.card_number; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.card_number IS 'Номер кредитной карты плательщика.';


--
-- Name: COLUMN payments.card_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.card_type IS 'Тип кредитной карты плательщика.';


--
-- Name: COLUMN payments.payment_purpose; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.payment_purpose IS 'Назначение платежа из payment_purposes_voc.';


--
-- Name: COLUMN payments.last_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.last_name IS 'Фамилия плательщика.';


--
-- Name: COLUMN payments.first_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.first_name IS 'Имя плательщика.';


--
-- Name: COLUMN payments.fio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.fio IS 'Фамилия и Имя плательщика.';


--
-- Name: COLUMN payments.email; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.email IS 'Адрес электронной почты плательщика.';


--
-- Name: COLUMN payments.telegram; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.telegram IS 'Имя Telegram плательщика.';


--
-- Name: COLUMN payments.participant_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.participant_id IS 'Плательщик.';


--
-- Name: COLUMN payments.time_create; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.time_create IS 'Дата создания.';


--
-- Name: COLUMN payments.payment_system; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.payments.payment_system IS 'Платёжная система из payment_systems_voc.';


--
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sessions_id_seq OWNER TO postgres;

--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    id integer DEFAULT nextval('public.sessions_id_seq'::regclass) NOT NULL,
    time_begin timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    time_end timestamp with time zone
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: TABLE sessions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.sessions IS 'Список сессий по обработке почты.';


--
-- Name: sessions_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions_tasks (
    id integer NOT NULL,
    task_uuid integer,
    session_id integer
);


ALTER TABLE public.sessions_tasks OWNER TO postgres;

--
-- Name: TABLE sessions_tasks; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.sessions_tasks IS 'Таблица связей между sessions и task.';


--
-- Name: sessions_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessions_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sessions_tasks_id_seq OWNER TO postgres;

--
-- Name: sessions_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sessions_tasks_id_seq OWNED BY public.sessions_tasks.id;


--
-- Name: task_steps_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_steps_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_steps_id_seq OWNER TO postgres;

--
-- Name: task_steps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_steps (
    id integer DEFAULT nextval('public.task_steps_id_seq'::regclass) NOT NULL,
    task_uuid integer NOT NULL,
    attempt integer NOT NULL,
    time_begin timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    time_end timestamp with time zone
);


ALTER TABLE public.task_steps OWNER TO postgres;

--
-- Name: TABLE task_steps; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.task_steps IS 'Шаги по обработке задачи.';


--
-- Name: COLUMN task_steps.attempt; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.task_steps.attempt IS 'Количество попыток';


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    time_begin timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    time_end timestamp with time zone,
    task_from character varying(2000),
    task_subject character varying(2000),
    task_body_type character varying(4),
    task_body_html text,
    task_body_text text,
    task_error character varying(4000),
    number_of_attempts integer,
    task_uuid integer NOT NULL,
    session_id integer NOT NULL,
    participant_id integer,
    attempt integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: TABLE tasks; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tasks IS 'Задача (по сути это отдельно письмо которое обрабатывается).';


--
-- Name: COLUMN tasks.attempt; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tasks.attempt IS 'Количество попыток работы с этим Task.';


--
-- Name: test_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_id_seq OWNER TO postgres;

--
-- Name: sessions_tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions_tasks ALTER COLUMN id SET DEFAULT nextval('public.sessions_tasks_id_seq'::regclass);


--
-- Data for Name: participants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participants (id, last_name, first_name, fio, email, telegram, time_begin, time_end, login, password, payment_date, number_of_days, deadline, comment, until_date, isblocked) FROM stdin;
\.


--
-- Data for Name: payment_purposes_voc; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment_purposes_voc (id, name, short_name) FROM stdin;
1	Друзья школы	ДШ
\.


--
-- Data for Name: payment_systems_voc; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payment_systems_voc (id, name, short_name) FROM stdin;
1	GetCourse	GC
2	PayKeeper	PK
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (task_uuid, name_of_service, payment_id, amount, sales_slip, card_number, card_type, id, payment_purpose, last_name, first_name, fio, email, telegram, participant_id, time_create, payment_system) FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (id, time_begin, time_end) FROM stdin;
\.


--
-- Data for Name: sessions_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions_tasks (id, task_uuid, session_id) FROM stdin;
\.


--
-- Data for Name: task_steps; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_steps (id, task_uuid, attempt, time_begin, time_end) FROM stdin;
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (time_begin, time_end, task_from, task_subject, task_body_type, task_body_html, task_body_text, task_error, number_of_attempts, task_uuid, session_id, participant_id, attempt) FROM stdin;
\.


--
-- Name: participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participants_id_seq', 163, true);


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_id_seq', 342, true);


--
-- Name: sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessions_id_seq', 62, true);


--
-- Name: sessions_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessions_tasks_id_seq', 644, true);


--
-- Name: task_steps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_steps_id_seq', 1, false);


--
-- Name: test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_id_seq', 1, false);


--
-- Name: participants participants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participants
    ADD CONSTRAINT participants_pkey PRIMARY KEY (id);


--
-- Name: payments payment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payment_pkey PRIMARY KEY (task_uuid);


--
-- Name: payment_purposes_voc payment_purposes_voc_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_purposes_voc
    ADD CONSTRAINT payment_purposes_voc_pkey PRIMARY KEY (id);


--
-- Name: payment_systems_voc payment_systems_voc_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_systems_voc
    ADD CONSTRAINT payment_systems_voc_pk PRIMARY KEY (id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sessions_tasks sessions_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions_tasks
    ADD CONSTRAINT sessions_tasks_pkey PRIMARY KEY (id);


--
-- Name: tasks task_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT task_pkey PRIMARY KEY (task_uuid);


--
-- Name: task_steps task_steps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_steps
    ADD CONSTRAINT task_steps_pkey PRIMARY KEY (id);


--
-- Name: fki_payment_participant_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_payment_participant_fk ON public.payments USING btree (participant_id);


--
-- Name: fki_payment_payment_systems_voc_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_payment_payment_systems_voc_fk ON public.payments USING btree (payment_system);


--
-- Name: fki_payment_type_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_payment_type_fk ON public.payments USING btree (payment_purpose);


--
-- Name: fki_sessions_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_sessions_fk ON public.tasks USING btree (session_id);


--
-- Name: fki_task_participant_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_task_participant_fk ON public.tasks USING btree (participant_id);


--
-- Name: fki_task_uuid_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_task_uuid_fk ON public.payments USING btree (task_uuid);


--
-- Name: fki_tasks_fk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_tasks_fk ON public.task_steps USING btree (task_uuid);


--
-- Name: idx_fio; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fio ON public.participants USING btree (fio);


--
-- Name: idx_mail; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_mail ON public.participants USING btree (email);


--
-- Name: idx_telegram; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_telegram ON public.participants USING btree (telegram);


--
-- Name: participants_pk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX participants_pk ON public.participants USING btree (id);


--
-- Name: task_step_pk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX task_step_pk ON public.task_steps USING btree (id);


--
-- Name: task_uuid_pk; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX task_uuid_pk ON public.tasks USING btree (task_uuid);


--
-- Name: payments payment_participant_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payment_participant_fk FOREIGN KEY (participant_id) REFERENCES public.participants(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: payments payment_payment_purpose_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payment_payment_purpose_fk FOREIGN KEY (payment_purpose) REFERENCES public.payment_purposes_voc(id) ON DELETE RESTRICT;


--
-- Name: payments payment_payment_systems_voc_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payment_payment_systems_voc_fk FOREIGN KEY (payment_system) REFERENCES public.payment_systems_voc(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: payments payment_task_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payment_task_fk FOREIGN KEY (task_uuid) REFERENCES public.tasks(task_uuid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: tasks task_participant_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT task_participant_fk FOREIGN KEY (participant_id) REFERENCES public.participants(id);


--
-- Name: tasks task_session_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT task_session_fk FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: task_steps task_steps_task_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_steps
    ADD CONSTRAINT task_steps_task_fk FOREIGN KEY (task_uuid) REFERENCES public.tasks(task_uuid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--


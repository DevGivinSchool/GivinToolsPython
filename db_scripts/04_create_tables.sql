-- Table: public.sessions

-- DROP TABLE public.sessions;

CREATE TABLE public.sessions
(
    id integer NOT NULL DEFAULT nextval('sessions_id_seq'::regclass),
    time_begin timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    time_end timestamp with time zone,
    CONSTRAINT sessions_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.sessions
    OWNER to postgres;
COMMENT ON TABLE public.sessions
    IS 'Список сессий по обработке почты.';
		
-- Table: public.payments_types_voc

-- DROP TABLE public.payments_types_voc;

CREATE TABLE public.payments_types_voc
(
    id integer NOT NULL,
    name character varying(2000) COLLATE pg_catalog."default" NOT NULL,
    short_name character varying(2000) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT payments_types_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.payments_types_voc
    OWNER to postgres;
COMMENT ON TABLE public.payments_types_voc
    IS 'Справочник типов платежей. ';

COMMENT ON COLUMN public.payments_types_voc.name
    IS 'Наименование типа платежа.';

COMMENT ON COLUMN public.payments_types_voc.short_name
    IS 'Сокращённое наименование типа платежа.';

INSERT INTO public.payments_types_voc(
	id, name, short_name)
	VALUES (1, 'Друзья школы', 'ДШ');
	
commit;

-- Table: public.participants

-- DROP TABLE public.participants;

CREATE TABLE public.participants
(
    id integer NOT NULL DEFAULT nextval('participants_id_seq'::regclass),
    last_name character varying(2000) COLLATE pg_catalog."default",
    first_name character varying(2000) COLLATE pg_catalog."default",
    fio character varying(4000) COLLATE pg_catalog."default",
    email character varying(254) COLLATE pg_catalog."default",
    telegram character varying(32) COLLATE pg_catalog."default",
    time_begin timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    time_end timestamp with time zone,
    CONSTRAINT participants_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.participants
    OWNER to postgres;
COMMENT ON TABLE public.participants
    IS 'Участники (участники различных мероприятий).';

-- Index: idx_fio

-- DROP INDEX public.idx_fio;

CREATE INDEX idx_fio
    ON public.participants USING btree
    (fio COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_mail

-- DROP INDEX public.idx_mail;

CREATE UNIQUE INDEX idx_mail
    ON public.participants USING btree
    (email COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: idx_telegram

-- DROP INDEX public.idx_telegram;

CREATE UNIQUE INDEX idx_telegram
    ON public.participants USING btree
    (telegram COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: participants_pk

-- DROP INDEX public.participants_pk;

CREATE UNIQUE INDEX participants_pk
    ON public.participants USING btree
    (id)
    TABLESPACE pg_default;

-- Table: public.tasks

-- DROP TABLE public.tasks;

CREATE TABLE public.tasks
(
    time_begin timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    time_end timestamp with time zone,
    task_from character varying(2000) COLLATE pg_catalog."default",
    task_subject character varying(2000) COLLATE pg_catalog."default",
    task_body_type character varying(4) COLLATE pg_catalog."default",
    task_body_html text COLLATE pg_catalog."default",
    task_body_text text COLLATE pg_catalog."default",
    task_error character varying(4000) COLLATE pg_catalog."default",
    number_of_attempts integer,
    task_uuid integer NOT NULL,
    session_id integer NOT NULL,
    participant_id integer,
    attempt integer NOT NULL,
    CONSTRAINT task_sessions_pkey PRIMARY KEY (task_uuid),
    CONSTRAINT participant_fk FOREIGN KEY (participant_id)
        REFERENCES public.participants (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT sessions_fk FOREIGN KEY (session_id)
        REFERENCES public.sessions (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT task_participant_fk FOREIGN KEY (participant_id)
        REFERENCES public.participants (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.tasks
    OWNER to postgres;
COMMENT ON TABLE public.tasks
    IS 'Задача (по сути это отдельно письмо которое обрабатывается).';

COMMENT ON COLUMN public.tasks.attempt
    IS 'Количество попыток';

-- Index: fki_sessions_fk

-- DROP INDEX public.fki_sessions_fk;

CREATE INDEX fki_sessions_fk
    ON public.tasks USING btree
    (session_id)
    TABLESPACE pg_default;

-- Index: fki_task_participant_fk

-- DROP INDEX public.fki_task_participant_fk;

CREATE INDEX fki_task_participant_fk
    ON public.tasks USING btree
    (participant_id)
    TABLESPACE pg_default;

-- Index: task_uuid_pk

-- DROP INDEX public.task_uuid_pk;

CREATE UNIQUE INDEX task_uuid_pk
    ON public.tasks USING btree
    (task_uuid)
    TABLESPACE pg_default;

-- Table: public.task_steps

-- DROP TABLE public.task_steps;

CREATE TABLE public.task_steps
(
    id integer NOT NULL DEFAULT nextval('task_steps_id_seq'::regclass),
    task_uuid integer NOT NULL,
    attempt integer NOT NULL,
    time_begin timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    time_end timestamp with time zone,
    CONSTRAINT task_steps_pkey PRIMARY KEY (id),
    CONSTRAINT tasks_fk FOREIGN KEY (task_uuid)
        REFERENCES public.tasks (task_uuid) MATCH SIMPLE
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.task_steps
    OWNER to postgres;
COMMENT ON TABLE public.task_steps
    IS 'Шаги по обработке задачи.';

COMMENT ON COLUMN public.task_steps.attempt
    IS 'Количество попыток';

-- Index: fki_tasks_fk

-- DROP INDEX public.fki_tasks_fk;

CREATE INDEX fki_tasks_fk
    ON public.task_steps USING btree
    (task_uuid)
    TABLESPACE pg_default;

-- Index: task_step_pk

-- DROP INDEX public.task_step_pk;

CREATE UNIQUE INDEX task_step_pk
    ON public.task_steps USING btree
    (id)
    TABLESPACE pg_default;

-- Table: public.payments

-- DROP TABLE public.payments;

CREATE TABLE public.payments
(
    task_uuid integer NOT NULL,
    name_of_service character varying(2000) COLLATE pg_catalog."default",
    payment_id character varying(2000) COLLATE pg_catalog."default",
    amount integer,
    sales_slip character varying(2000) COLLATE pg_catalog."default",
    card_number character varying(2000) COLLATE pg_catalog."default",
    card_type character varying(2000) COLLATE pg_catalog."default",
    id integer NOT NULL DEFAULT nextval('payments_id_seq'::regclass),
    payment_type integer NOT NULL,
    last_name character varying(2000) COLLATE pg_catalog."default",
    first_name character varying(2000) COLLATE pg_catalog."default",
    fio character varying(4000) COLLATE pg_catalog."default",
    mail character varying(254) COLLATE pg_catalog."default",
    telegram character varying(32) COLLATE pg_catalog."default",
    participant_id integer,
    time_create timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT payment_participant_fk FOREIGN KEY (participant_id)
        REFERENCES public.participants (id) MATCH SIMPLE
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    CONSTRAINT payment_type_fk FOREIGN KEY (payment_type)
        REFERENCES public.payments_types_voc (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE RESTRICT,
    CONSTRAINT task_uuid_fk FOREIGN KEY (task_uuid)
        REFERENCES public.tasks (task_uuid) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.payments
    OWNER to postgres;

COMMENT ON COLUMN public.payments.task_uuid
    IS 'Уникальное UUID задачи(письма) в котором был этот платёж.';

COMMENT ON COLUMN public.payments.name_of_service
    IS 'Наименование услуги (как в письме).';

COMMENT ON COLUMN public.payments.payment_id
    IS 'ID платежа (как в письме).';

COMMENT ON COLUMN public.payments.amount
    IS 'Сумма платежа.';

COMMENT ON COLUMN public.payments.sales_slip
    IS 'Кассовый чек 54-ФЗ (ссылка на него).';

COMMENT ON COLUMN public.payments.card_number
    IS 'Номер кредитной карты плательщика.';

COMMENT ON COLUMN public.payments.card_type
    IS 'Тип кредитной карты плательщика.';

COMMENT ON COLUMN public.payments.payment_type
    IS 'Тип платежа: (Друзья Школы, ПТО, ОК и т.п.).';

COMMENT ON COLUMN public.payments.participant_id
    IS 'Плательщик.';

-- Index: fki_payment_participant_fk

-- DROP INDEX public.fki_payment_participant_fk;

CREATE INDEX fki_payment_participant_fk
    ON public.payments USING btree
    (participant_id)
    TABLESPACE pg_default;

-- Index: fki_payment_type_fk

-- DROP INDEX public.fki_payment_type_fk;

CREATE INDEX fki_payment_type_fk
    ON public.payments USING btree
    (payment_type)
    TABLESPACE pg_default;

-- Index: fki_task_uuid_fk

-- DROP INDEX public.fki_task_uuid_fk;

CREATE INDEX fki_task_uuid_fk
    ON public.payments USING btree
    (task_uuid)
    TABLESPACE pg_default;

commit;
		
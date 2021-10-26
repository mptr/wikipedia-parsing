

-- SET statement_timeout = 0;
-- SET lock_timeout = 0;
-- SET idle_in_transaction_session_timeout = 0;
-- SET client_encoding = 'UTF8';
-- SET standard_conforming_strings = on;
-- SELECT pg_catalog.set_config('search_path', '', false);
-- SET check_function_bodies = false;
-- SET xmloption = content;
-- SET client_min_messages = warning;
-- SET row_security = off;


CREATE TYPE public.ambiguitiy_type AS ENUM (
    'link',
    'spacy',
    'redirect'
);

CREATE TYPE public.entity_ner_type AS ENUM (
    'CARDINAL',
    'DATE',
    'EVENT',
    'FAC',
    'GPE',
    'LANGUAGE',
    'LAW',
    'LOC',
    'MONEY',
    'NORP',
    'ORDINAL',
    'ORG',
    'PERCENT',
    'PERSON',
    'PRODUCT',
    'QUANTITY',
    'TIME',
    'WORK_OF_ART'
);

CREATE TABLE public.ambiguities (
    id integer NOT NULL,
    base character varying(255) NOT NULL,
    alt character varying(255) NOT NULL,
    kind public.ambiguitiy_type NOT NULL
);

ALTER TABLE public.ambiguities ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.ambiguities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.pages (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    wikidata_id character varying(50)
);

ALTER TABLE public.pages ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.pages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.sentences (
    id integer NOT NULL,
    text character varying(5000) NOT NULL,
    page_id integer NOT NULL
);

ALTER TABLE public.sentences ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.sentences_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.entities (
    id integer NOT NULL,
    start integer NOT NULL,
    "end" integer NOT NULL,
    kind public.entity_ner_type NOT NULL,
    wikidata_id character varying(50),
    sentence_id integer NOT NULL
);

ALTER TABLE public.entities ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.entities_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY public.ambiguities
    ADD CONSTRAINT ambiguities_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.pages
    ADD CONSTRAINT pages_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.sentences
    ADD CONSTRAINT sentences_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.entities
    ADD CONSTRAINT entities_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.sentences
    ADD CONSTRAINT pages_fk FOREIGN KEY (page_id) REFERENCES public.pages(id) NOT VALID;

ALTER TABLE ONLY public.entities
    ADD CONSTRAINT sentences_fk FOREIGN KEY (sentence_id) REFERENCES public.sentences(id) NOT VALID;

CREATE OR REPLACE VIEW public."Sentences"
 AS
 SELECT s.id,
    s.text,
    s.page_id,
    count(e.id) AS entity_count
   FROM sentences s
     RIGHT JOIN entities e ON s.id = e.sentence_id
  GROUP BY s.id
  ORDER BY (count(e.id)) DESC;

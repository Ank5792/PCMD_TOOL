--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: discussion_meta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discussion_meta (
    id integer NOT NULL,
    discussion_topic character varying(100) NOT NULL,
    status character varying(20) NOT NULL,
    host_username character varying(50) NOT NULL
);


ALTER TABLE public.discussion_meta OWNER TO postgres;

--
-- Name: discussion_meta_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discussion_meta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.discussion_meta_id_seq OWNER TO postgres;

--
-- Name: discussion_meta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discussion_meta_id_seq OWNED BY public.discussion_meta.id;


--
-- Name: discussion_meta id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion_meta ALTER COLUMN id SET DEFAULT nextval('public.discussion_meta_id_seq'::regclass);


--
-- Data for Name: discussion_meta; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discussion_meta (id, discussion_topic, status, host_username) FROM stdin;
1	Microcode	open	ankita
\.


--
-- Name: discussion_meta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discussion_meta_id_seq', 17, true);


--
-- Name: discussion_meta discussion_meta_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion_meta
    ADD CONSTRAINT discussion_meta_pkey PRIMARY KEY (id);


--
-- Name: discussion_meta unique_discussion_topic; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion_meta
    ADD CONSTRAINT unique_discussion_topic UNIQUE (discussion_topic);


--
-- PostgreSQL database dump complete
--


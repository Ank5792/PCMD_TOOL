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
-- Name: discussion_microcode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discussion_microcode (
    id integer NOT NULL,
    discussion_topic character varying(100) NOT NULL,
    user_name character varying(50) NOT NULL,
    datetime character varying(50) NOT NULL,
    comment character varying(500) NOT NULL
);


ALTER TABLE public.discussion_microcode OWNER TO postgres;

--
-- Name: discussion_microcode_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discussion_microcode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.discussion_microcode_id_seq OWNER TO postgres;

--
-- Name: discussion_microcode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discussion_microcode_id_seq OWNED BY public.discussion_microcode.id;


--
-- Name: discussion_microcode id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion_microcode ALTER COLUMN id SET DEFAULT nextval('public.discussion_microcode_id_seq'::regclass);


--
-- Data for Name: discussion_microcode; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discussion_microcode (id, discussion_topic, user_name, datetime, comment) FROM stdin;
1	Microcode	ankita	8/18/2023, 7:38:20 AM	hi
2	Microcode	ankita	8/18/2023, 8:17:57 AM	hello
3	Microcode	ankita	8/18/2023, 8:18:02 AM	how are you
4	Microcode	ankita	8/18/2023, 8:18:07 AM	i am fine
5	Microcode	ankita	8/18/2023, 8:18:10 AM	testing 1
6	Microcode	ankita	8/18/2023, 8:18:13 AM	byeee
7	Microcode	ankita	8/21/2023, 2:50:01 PM	ki
8	Microcode	ankita	8/21/2023, 2:50:14 PM	my name is anku
9	Microcode	ankita	8/21/2023, 2:50:18 PM	byee
10	Microcode	ankita	8/21/2023, 2:51:30 PM	hi tejas
11	Microcode	tejas	8/21/2023, 2:51:37 PM	hi ankita
12	Microcode	ankita	8/21/2023, 2:51:51 PM	testing ok
13	Microcode	tejas	8/21/2023, 2:51:58 PM	got it
14	Microcode	ankita	8/21/2023, 2:52:05 PM	byee
15	Microcode	tejas	8/21/2023, 2:52:10 PM	byee
16	Microcode	ankita	8/24/2023, 10:41:00 AM	Good morning
\.


--
-- Name: discussion_microcode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discussion_microcode_id_seq', 16, true);


--
-- Name: discussion_microcode discussion_microcode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion_microcode
    ADD CONSTRAINT discussion_microcode_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--


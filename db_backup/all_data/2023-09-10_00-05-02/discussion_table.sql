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
-- Name: discussion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discussion (
    id integer NOT NULL,
    discussion_topic character varying(100) NOT NULL,
    user_name character varying(50) NOT NULL,
    datetime character varying(50) NOT NULL,
    comment character varying(500) NOT NULL
);


ALTER TABLE public.discussion OWNER TO postgres;

--
-- Name: discussion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discussion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.discussion_id_seq OWNER TO postgres;

--
-- Name: discussion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discussion_id_seq OWNED BY public.discussion.id;


--
-- Name: discussion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion ALTER COLUMN id SET DEFAULT nextval('public.discussion_id_seq'::regclass);


--
-- Data for Name: discussion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discussion (id, discussion_topic, user_name, datetime, comment) FROM stdin;
1	Microcode	ankita	8/15/2023, 10:43:31 PM	hi
2	Microcode	New User	8/15/2023, 10:44:21 PM	hello
3	Microcode	ankita	8/15/2023, 10:46:53 PM	how are you?
4	Microcode	New User	8/15/2023, 10:47:11 PM	i am good!!!
5	Microcode	tejas	8/16/2023, 4:34:43 AM	hi
6	Microcode	tejas	8/16/2023, 4:35:22 AM	hello
7	Microcode	nsonal	8/16/2023, 4:50:07 AM	testing 2
8	Microcode	nsonal	8/16/2023, 4:50:16 AM	testing 3
9	Microcode	nsonal	8/16/2023, 4:51:31 AM	testing 2
10	Microcode	ankita	8/17/2023, 10:34:15 PM	hi
11	Microcode	ankita	8/17/2023, 10:34:19 PM	hello
12	Microcode	ankita	8/17/2023, 10:43:27 PM	hy
13	Microcode	ankita	8/17/2023, 11:04:03 PM	hi
14	Microcode	ankita	8/17/2023, 11:04:06 PM	hello
15	Microcode	ankita	8/18/2023, 12:43:44 AM	hi
16	Microcode	ankita	8/18/2023, 12:50:22 AM	mine
17	Microcode	ankita	8/18/2023, 2:12:37 AM	my name is anku
\.


--
-- Name: discussion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discussion_id_seq', 17, true);


--
-- Name: discussion discussion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion
    ADD CONSTRAINT discussion_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--


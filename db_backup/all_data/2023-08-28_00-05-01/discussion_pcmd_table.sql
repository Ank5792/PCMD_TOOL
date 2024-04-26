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
-- Name: discussion_pcmd; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discussion_pcmd (
    id integer NOT NULL,
    discussion_topic character varying(100) NOT NULL,
    user_name character varying(50) NOT NULL,
    datetime character varying(50) NOT NULL,
    comment character varying(500) NOT NULL
);


ALTER TABLE public.discussion_pcmd OWNER TO postgres;

--
-- Name: discussion_pcmd_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.discussion_pcmd_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.discussion_pcmd_id_seq OWNER TO postgres;

--
-- Name: discussion_pcmd_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.discussion_pcmd_id_seq OWNED BY public.discussion_pcmd.id;


--
-- Name: discussion_pcmd id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion_pcmd ALTER COLUMN id SET DEFAULT nextval('public.discussion_pcmd_id_seq'::regclass);


--
-- Data for Name: discussion_pcmd; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discussion_pcmd (id, discussion_topic, user_name, datetime, comment) FROM stdin;
1	PCMD	ankita	8/18/2023, 8:26:07 AM	hi
2	PCMD	ankita	8/18/2023, 8:26:12 AM	hello
3	PCMD	ankita	8/18/2023, 8:27:04 AM	byee
\.


--
-- Name: discussion_pcmd_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.discussion_pcmd_id_seq', 3, true);


--
-- Name: discussion_pcmd discussion_pcmd_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discussion_pcmd
    ADD CONSTRAINT discussion_pcmd_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--


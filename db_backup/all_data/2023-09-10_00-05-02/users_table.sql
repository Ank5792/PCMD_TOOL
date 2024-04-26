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
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    idsid character varying(255) NOT NULL,
    first_login timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    profile_img_name character varying(255) DEFAULT 'user.jpg'::character varying,
    is_admin boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, idsid, first_login, profile_img_name, is_admin) FROM stdin;
2	vinay.p@intel.com	New User	2023-08-09 18:51:20.416729	user.jpg	f
1	nirmal.sonal@intel.com	nsonal	2023-08-09 19:49:54.951243	user.jpg	t
5	shelly.kishore@intel.com	New User	2023-08-09 20:09:33.818185	user.jpg	f
7	vinay1.kumar@intel.com	vinay1	2023-08-09 23:49:55.212338	user.jpg	f
6	ankita.hora@intel.com	ankita	2023-08-09 22:42:54.978611	user.jpg	t
4	prathap.m.j@intel.com	New User	2023-08-09 19:56:21.172287	user.jpg	t
9	paluri.vinay@intel.com	paluri	2023-08-16 01:04:02.004058	user.jpg	f
11	tejas.kawale@intel.com	tejas	2023-08-16 04:33:37.830771	user.jpg	f
12	marek.bartosinski@intel.com	marek	2023-08-16 13:48:13.848906	user.jpg	f
13	dhaneeswaran.r@intel.com	dhaneeswaran	2023-08-17 03:18:51.031003	user.jpg	f
14	anandha.basker.s@intel.com	anandha	2023-08-18 05:20:34.702054	user.jpg	f
15	prathap.srinivas@intel.com	prathap	2023-08-23 02:38:04.862631	user.jpg	f
16	kunal.mahajan@intel.com	kunal	2023-08-28 21:36:35.682999	user.jpg	f
17	umamaheswari.govindaraj@intel.com	umamaheswari	2023-09-04 22:45:11.945376	user.jpg	f
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 17, true);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--


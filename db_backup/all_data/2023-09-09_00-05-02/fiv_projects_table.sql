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
-- Name: fiv_projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fiv_projects (
    project_id integer NOT NULL,
    owner character varying(255) NOT NULL,
    short_description text NOT NULL,
    description text NOT NULL,
    current_status character varying(30) NOT NULL,
    image_path character varying(50),
    wiki_link character varying(200),
    jira_link character varying(200),
    ags_link character varying(200),
    tool_links text[],
    tool_devs text[] NOT NULL,
    tool_name character varying(200) NOT NULL,
    CONSTRAINT fiv_projects_description_check CHECK ((length(description) <= 3000)),
    CONSTRAINT fiv_projects_short_description_check CHECK ((length(short_description) <= 500))
);


ALTER TABLE public.fiv_projects OWNER TO postgres;

--
-- Name: fiv_projects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fiv_projects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fiv_projects_id_seq OWNER TO postgres;

--
-- Name: fiv_projects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fiv_projects_id_seq OWNED BY public.fiv_projects.project_id;


--
-- Name: fiv_projects project_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fiv_projects ALTER COLUMN project_id SET DEFAULT nextval('public.fiv_projects_id_seq'::regclass);


--
-- Data for Name: fiv_projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fiv_projects (project_id, owner, short_description, description, current_status, image_path, wiki_link, jira_link, ags_link, tool_links, tool_devs, tool_name) FROM stdin;
5	nirmal.sonal@intel.com	FIV End to End Autonomous Service Tool provides a user friendly interface where its users can access all the information regarding tools created in FIV.	EAST aims to be a one-stop solution where users can access as well as get familiar with FIV deployed tools. Users can access all the tools with a single click on the interface. They can also find information regarding the progress of the under-development tool and information on how to communicate with the developers of the said tool. Users need to just sign-up for FEAST (with their intel Email ID and Password).\r\n\r\nTo list a project on FEAST, a developer can provide the following information to either of the developers for FEAST. The required information is:\r\n\r\n1. Tool Name: The Name of the tool to be displayed (acronyms\r\nare optimal)\r\n\r\n2. Owner Email: Email Id to which the tool will be linked on the FEAST app. The owner will be able to edit the details later\r\n\r\n3. Short Description: 5-6 lines introduction that will be shown to the user on the front page.\r\n\r\n4. Description: Complete the Textual Description that you would like to be shown to the user.\r\n\r\n5. current Status: It can be either "Under Development" or "Deployed and Running".\r\n\r\n6. Tool Type: "Web Based" or "Offline setup"\r\n\r\n7. Working Links: IP or address where the tool can be accessed (if it is deployed) or where the setup can be downloaded. Multiple links can also be provided.\r\n\r\n8. Wiki Link: If applicable \r\n\r\nn9. Jira Link: If applicable (where projects progress is being tracked)\r\n\r\n10. Developer Email: Email Ids of the developer currently working on the tool\r\n\r\n11: AGS Link: If applicable (where the user needs to request access).	web_prod	 	 	 	 	{http://goto/FEAST}	{prathap.m.j@intel.com,nirmal.sonal@intel.com}	FEAST
3	vinay.p@intel.com	FIV Smart Patch Analytics and Reconnaissance (FSPARC) is a tool that helps analyze whether a bug fix on one project should be ported to other relevant projects or not, depending on POR features.	System firmware (BIOS) code is common across different server programs to some extent. \r\n\r\nFirmware fixes happening on one program are not diligently ported for all the applicable programs. This leads to raising new firmware defects at a later point of time. In such cases, there is a risk associated in leveraging validation results from main program to derivative programs.\r\n\tFSARC aims to automate this process. The tool takes two projects (one primary and one secondary) as input. It fetches the details of raised sightings on Primary Project's query ID and then tries to get patch details from GitHub using its API.\r\n\t\r\n\tThe tool then checks whether the downloaded patch is present in secondary project's source code. If the changes are present, then the associated sighting is marked as "ported" as it is marked as "porting missing".\r\n\t\r\n\tCurrently the tool only checks for patches in Program Specific (Rp) Packages. It only fetches patch information from GitHub, so if ISE has Gerrit Link then it will be discarded.	web_prod	 	https://wiki.ith.intel.com/pages/viewpage.action?spaceKey=ITSFID&title=FSPARC-v1	 	 	{http://10.223.244.60:5095/}	{vinay.p@intel.com,naga.k@intel.com,kunal.mahajan@intel.com}	FSPARC
2	nirmal.sonal@intel.com	FIV Sysdebug Assist Tool (FSAT) is a one stop shop for SysDebug engineer to get all kinds of information like Bios Check-ins, Ingredient Comparison etc. in less than 5 clicks.	FSAT provides a highly customizable yet user-friendly way for a Sys-Debug engineer to get information of various kinds with minimum clicks. The tool currently supports comparing:\r\n\r\n1. Ingredient Comparison: Here, a user can specify any two D-Labels belonging to the same project and the tool will provide them with a table depicting the Ingredients changes. A one-click solution is also provided where the tool will provide the user with an Ingredient difference table for each pair of builds where regression has occurred.\r\n\r\n2. Bios Check-Ins: Users can specify any two D-Labels and the tool will provide them with the information regarding all the sightings/check-ins performed between them. Other than specifying the D-Labels, users can also provide the SHA Labels to specify their desired range.\r\n3. Micro-patching: The user can provide the micro-patch and the binary package and the tool will allow the user to download the patched binary directly without ever dealing with XMLCLI on their side. Users can also select to overwrite specific patches already made on their uploaded package or remove all patches or simply add new ones.	web_prod	 	https://wiki.ith.intel. com/pages/viewpage.action?pageId=2835293270	https://jira.devtools.intel.com/browse/ISB0-2931	 	{http://goto/FSAT,http://10.66.244.40:5050}	{nirmal.sonal@intel.com,prathap.m.j@intel.com}	FSAT
4	abhishek1.mishra@intel.com	AI Assistance tool for classifying SW req. in testable/non-testable category and recommending test cases for the testable requirements.	Any platform’s scope is done through a list of requirements & validation teams are responsible for covering those requirements through test cases. Today, the assessment of those requirements & creation of test contents is done manually by engineers & consumes much time. ARVA is an AI tool that uses NLP and a fine-tuned BERT variant to assess information sufficiency and testability for the requirements. The tool recommends existing test cases that it can find in the database; if there are no existing test cases, the model should recommend newer test cases.	web_dev	 	 	 	 	{""}	{abhishek1.mishra@intel.com,suchana.chandra@intel.com,amruta.das@intel.com}	ARVA - WIP
6	abhishek1.mishra@intel.com	Tool to compare 2 or more platforms for Gen-on-gen improvement using the bug-TCD relationship. Optimise bug per test by finding domains/test categories/methods with best ROI. Automatically extracts test case relationship from bugs with no test case relationship (>90%).	DuET stands for Domain Upgrade and Enhancement Tool.\r\n\r\nDuET tool analyses the relationship between bugs and test cases to draw insights for better Bug ROI.\r\nIdentifies areas for improvement and provides recommendations for enhancement.\r\nInsights for improving test content for domain/program.\r\nMaximize Bug capture ROI.\r\nHigher quality products and reduced risk of customer escapes.\r\nDuET provides possible ways for a program/domain to identify areas to improve.	web_prod	 	https://wiki.ith.intel.com/pages/viewpage.action?pageId=2724902824	https://jira.devtools.intel.com/browse/DUETA	 	{https://goto.intel.com/duetool}	{abhishek1.mishra@intel.com,suchana.chandra@intel.com,amruta.das@intel.com}	DuET
7	abhishek1.mishra@intel.com	BRNG is a portal that allows easy and fast release notes generation for any FIV project.	BRNG stands for Bios Release Notes Genie.\r\nBRNG is a portal that allows easy and fast release notes generation for any FIV project.\r\n\r\n•\tInstant Refresh (< 10s)\r\n•\t< 1 day for new platform setup\r\n•\tBIOS commits to HSDes bug/feature relationship\r\n•\tPlatform-wise categorization of release notes\r\n•\tSingle HTML file for easy sharing\r\n•\tD-label selection/SHA-ID selection/artifactory url linking for easy release notes generation\r\n•\tREST API availability planned for easy integration in other projects	web_prod	 	 	 	 	{https://goto.intel.com/fiv-brng}	{"abhishek1.mishra@intel.com, kunal.mahajan@intel.com"}	BRNG
10	nirmal.sonal@intel.com	This tool creates pull requests related to ingredient updates without downloading the source code and editing any files manually by feeding the required details from the GUI-based web page.	This tool creates pull requests related to ingredient updates without downloading the source code and editing any files manually by feeding the required details from the GUI-based web page.	web_dev	 	 	 	 	{""}	{nirmal.sonal@intel.com}	FDBin PR Generator - WIP
8	abhishek1.mishra@intel.com	KURG takes in current release IFWI and older release IFWI and identifies all changes on the level of BIOS knobs and settings. It then automatically identifies possible BIOS check-ins explaining reason for those changes. It also generates an email that can be used for reference or shared with stakeholders.	KURG takes in current release IFWI and older release IFWI and identifies all changes on the level of BIOS knobs and settings. It then automatically identifies possible BIOS check-ins explaining the reason for those changes. It also generates an email that can be used for reference or shared with stakeholders.	web_dev	 	 	 	 	{""}	{abhishek1.mishra@intel.com,shaik.hussain@intel.com}	KURG
9	bhavana.arunkumar@intel.com	FIV Report Automation Service (FRAS) allows its user to automate sending reports via mail. It sup ports PBI dashboards and HSD Queries as data sources and support wide range of customizations.	FRAS provides an easy way for its users to automate the project reports that are usually generated manually by project leads. Creating manual reports every day is a time-consuming task and is error-prone. FRAS allows several ways to automate a report depending on the data source and the amount of customizations needed:\r\n\r\n1. One-step personal subscription: Users can simply provide the URL of their desired Power-BI dashboard or select from the ones that are already listed.\r\n\r\n2. Basic-configuration PBI report: The option is just like the former. However, the user can provide a list of PDL here and all of them will receive the report. PDL can be any valid @intel.com email.\r\n\r\n3. Advance Configuration PBI report: Unlike the other options, the user has the flexibility here to edit and customize the report as per their liking. User can provide their own banner, apply filters, and select specific dashboard pages they want in their report instead of adding all. They can customize text at the top and bottom of the mail, and add some static images too.\r\n\r\n4. HSD Report: Instead of providing a PBI URL, users can provide a query ID of their project ID and the tool will return them a list of tables that they can add to their report. For example, the user can select a table containing open P1-bugs along with a table containing weekly sightings summary, etc. The tool provides flexibility to users to select as many tables as their liking.\r\n\r\n5. PBI + HSD reports: As the name suggests, here user can craft a report containing both PBI and HSD data. \r\n\r\nIn all of these cases, the tool will allow users to schedule reports at their desired time (IST) and frequency (daily/weekly/biweekly). Once scheduled, the report is linked to the user profile. They can edit, delete or trigger the report from there whenever desired.	web_prod	 	 https://wiki.ith.intel.com/pages/viewpage.action?pageId=2584538935	 https://jira.devtools.intel.com/browse/ISB0-2052	 	{http://goto/FRAS}	{bhavana.arunkumar@intel.com,nirmal.sonal@intel.com}	FRAS
11	nirmal.sonal@intel.com	short description.	complete description.	web_prod	 	 	 	 	{http://goto/FEAST}	{nirmal.sonal@intel.com,prathap.m.j@intel.com}	Example Updated
1	nirmal.sonal@intel.com	This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.	This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.This tool will help in finding duplicate HSDES IDs, by providing either the Title and Description or by directly providing the article ID.	web_dev	 	 	 	 	{http://goto/FEAST}	{nirmal.sonal@intel.com,abhishek1.mishra@intel.com}	Duplicate Finder - WIP
\.


--
-- Name: fiv_projects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fiv_projects_id_seq', 11, true);


--
-- Name: fiv_projects fiv_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fiv_projects
    ADD CONSTRAINT fiv_projects_pkey PRIMARY KEY (project_id);


--
-- PostgreSQL database dump complete
--


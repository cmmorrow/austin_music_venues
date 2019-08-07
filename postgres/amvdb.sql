--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2 (Debian 11.2-1.pgdg90+1)
-- Dumped by pg_dump version 11.3

-- Started on 2019-08-06 00:17:49 CDT

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

SET default_with_oids = false;

CREATE ROLE demo WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  CREATEDB
  NOCREATEROLE
  NOREPLICATION;

--
-- TOC entry 197 (class 1259 OID 24579)
-- Name: address; Type: TABLE; Schema: public; Owner: demo
--

CREATE TABLE public.address (
    id integer NOT NULL,
    street character varying NOT NULL,
    city character varying,
    state character varying(2),
    zip character varying,
    inserted timestamp without time zone
);


ALTER TABLE public.address OWNER TO demo;

--
-- TOC entry 196 (class 1259 OID 24577)
-- Name: address_id_seq; Type: SEQUENCE; Schema: public; Owner: demo
--

CREATE SEQUENCE public.address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.address_id_seq OWNER TO demo;

--
-- TOC entry 2898 (class 0 OID 0)
-- Dependencies: 196
-- Name: address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: demo
--

ALTER SEQUENCE public.address_id_seq OWNED BY public.address.id;


--
-- TOC entry 201 (class 1259 OID 24606)
-- Name: rating; Type: TABLE; Schema: public; Owner: demo
--

CREATE TABLE public.rating (
    id integer NOT NULL,
    venue_id integer,
    score integer,
    review character varying,
    inserted timestamp without time zone
);


ALTER TABLE public.rating OWNER TO demo;

--
-- TOC entry 200 (class 1259 OID 24604)
-- Name: rating_id_seq; Type: SEQUENCE; Schema: public; Owner: demo
--

CREATE SEQUENCE public.rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rating_id_seq OWNER TO demo;

--
-- TOC entry 2899 (class 0 OID 0)
-- Dependencies: 200
-- Name: rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: demo
--

ALTER SEQUENCE public.rating_id_seq OWNED BY public.rating.id;


--
-- TOC entry 199 (class 1259 OID 24590)
-- Name: venue; Type: TABLE; Schema: public; Owner: demo
--

CREATE TABLE public.venue (
    id integer NOT NULL,
    address_id integer,
    name character varying,
    closed boolean,
    inserted timestamp without time zone,
    image_url character varying,
    description character varying
);


ALTER TABLE public.venue OWNER TO demo;

--
-- TOC entry 198 (class 1259 OID 24588)
-- Name: venue_id_seq; Type: SEQUENCE; Schema: public; Owner: demo
--

CREATE SEQUENCE public.venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.venue_id_seq OWNER TO demo;

--
-- TOC entry 2900 (class 0 OID 0)
-- Dependencies: 198
-- Name: venue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: demo
--

ALTER SEQUENCE public.venue_id_seq OWNED BY public.venue.id;


--
-- TOC entry 2755 (class 2604 OID 24582)
-- Name: address id; Type: DEFAULT; Schema: public; Owner: demo
--

ALTER TABLE ONLY public.address ALTER COLUMN id SET DEFAULT nextval('public.address_id_seq'::regclass);


--
-- TOC entry 2757 (class 2604 OID 24609)
-- Name: rating id; Type: DEFAULT; Schema: public; Owner: demo
--

ALTER TABLE ONLY public.rating ALTER COLUMN id SET DEFAULT nextval('public.rating_id_seq'::regclass);


--
-- TOC entry 2756 (class 2604 OID 24593)
-- Name: venue id; Type: DEFAULT; Schema: public; Owner: demo
--

ALTER TABLE ONLY public.venue ALTER COLUMN id SET DEFAULT nextval('public.venue_id_seq'::regclass);


--
-- TOC entry 2759 (class 2606 OID 24587)
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: demo
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (id);


--
-- TOC entry 2763 (class 2606 OID 24614)
-- Name: rating rating_pkey; Type: CONSTRAINT; Schema: public; Owner: demo
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_pkey PRIMARY KEY (id);


--
-- TOC entry 2761 (class 2606 OID 24598)
-- Name: venue venue_pkey; Type: CONSTRAINT; Schema: public; Owner: demo
--

ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_pkey PRIMARY KEY (id);


--
-- TOC entry 2765 (class 2606 OID 24615)
-- Name: rating rating_venue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: demo
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_venue_id_fkey FOREIGN KEY (venue_id) REFERENCES public.venue(id);


--
-- TOC entry 2764 (class 2606 OID 24599)
-- Name: venue venue_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: demo
--

ALTER TABLE ONLY public.venue
    ADD CONSTRAINT venue_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.address(id);


-- Completed on 2019-08-06 00:17:49 CDT

--
-- PostgreSQL database dump complete
--


--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

-- Started on 2025-05-27 12:55:55

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 3079 OID 19749)
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- TOC entry 6098 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- TOC entry 2 (class 3079 OID 18468)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 6099 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- TOC entry 4 (class 3079 OID 20549)
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- TOC entry 6100 (class 0 OID 0)
-- Dependencies: 4
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


--
-- TOC entry 666 (class 1255 OID 20132)
-- Name: geo_features_search_vector_update(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.geo_features_search_vector_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.search_vector := 
    to_tsvector('english', 
      coalesce(NEW.properties->>'name', '') || ' ' ||
      coalesce(NEW.properties->>'category', '') || ' ' ||
      coalesce(NEW.properties->>'sub_category', '') || ' ' ||
      coalesce(NEW.properties->>'highway', '') || ' ' ||
      coalesce(NEW.properties->>'railway', '') || ' ' ||
      coalesce(NEW.properties->>'source', '') || ' ' ||
      coalesce(NEW.properties->>'geohash_id', '') || ' ' ||
      coalesce(NEW.properties->>'status', '') || ' ' ||
      coalesce(NEW.properties->>'lane', '') || ' ' ||
      coalesce(NEW.properties->>'type', '')
    );
  RETURN NEW;
END
$$;


ALTER FUNCTION public.geo_features_search_vector_update() OWNER TO postgres;

--
-- TOC entry 1135 (class 1255 OID 19892)
-- Name: jsonb_to_text(jsonb); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.jsonb_to_text(jsonb) RETURNS text
    LANGUAGE sql IMMUTABLE
    AS $_$
SELECT string_agg(value::text, ' ')
FROM jsonb_each_text($1)
$_$;


ALTER FUNCTION public.jsonb_to_text(jsonb) OWNER TO postgres;

--
-- TOC entry 487 (class 1255 OID 19920)
-- Name: update_properties_text(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_properties_text() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.properties_text :=
    to_tsvector('english', 
      jsonb_to_text(NEW.properties)); -- assuming JSONB properties
  RETURN NEW;
END
$$;


ALTER FUNCTION public.update_properties_text() OWNER TO postgres;

--
-- TOC entry 845 (class 1255 OID 20546)
-- Name: update_search_vector(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_search_vector() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.search_vector := to_tsvector('english', NEW.properties::text);
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_search_vector() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 226 (class 1259 OID 19615)
-- Name: HighwayDetails; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."HighwayDetails" (
    longitude numeric(10,8) NOT NULL,
    latitude numeric(10,8) NOT NULL,
    name character varying(255) NOT NULL,
    category character varying(255) NOT NULL,
    sub_category character varying(255) NOT NULL,
    highway character varying(255) NOT NULL,
    source character varying(255) NOT NULL,
    geohash_id character varying(255) NOT NULL,
    status character varying(255) NOT NULL,
    lane character varying(255) NOT NULL,
    type character varying(255) NOT NULL
);


ALTER TABLE public."HighwayDetails" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 18465)
-- Name: RailwayStations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."RailwayStations" (
    longitude numeric(10,8) NOT NULL,
    latitude numeric(10,8) NOT NULL,
    name character varying(255) NOT NULL,
    category character varying(255) NOT NULL,
    railway character varying(255) NOT NULL,
    source character varying(255) NOT NULL,
    sub_category character varying(255) NOT NULL,
    geohash_id character varying(255) NOT NULL,
    type character varying(255) NOT NULL,
    location public.geography(Point,4326),
    id integer NOT NULL,
    search_vector tsvector
);


ALTER TABLE public."RailwayStations" OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 19629)
-- Name: RailwayStations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."RailwayStations_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."RailwayStations_id_seq" OWNER TO postgres;

--
-- TOC entry 6101 (class 0 OID 0)
-- Dependencies: 227
-- Name: RailwayStations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."RailwayStations_id_seq" OWNED BY public."RailwayStations".id;


--
-- TOC entry 229 (class 1259 OID 20003)
-- Name: features; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.features (
    id integer NOT NULL,
    properties jsonb,
    geom public.geometry,
    search_vector tsvector
);


ALTER TABLE public.features OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 20002)
-- Name: features_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.features_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.features_id_seq OWNER TO postgres;

--
-- TOC entry 6102 (class 0 OID 0)
-- Dependencies: 228
-- Name: features_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.features_id_seq OWNED BY public.features.id;


--
-- TOC entry 231 (class 1259 OID 20149)
-- Name: geo_features; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.geo_features (
    id integer NOT NULL,
    feature_type text,
    properties jsonb,
    geometry public.geometry,
    geom_type text,
    coordinates jsonb,
    search_vector tsvector
);


ALTER TABLE public.geo_features OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 20148)
-- Name: geo_features_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.geo_features_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.geo_features_id_seq OWNER TO postgres;

--
-- TOC entry 6103 (class 0 OID 0)
-- Dependencies: 230
-- Name: geo_features_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.geo_features_id_seq OWNED BY public.geo_features.id;


--
-- TOC entry 232 (class 1259 OID 20414)
-- Name: semantic_search; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.semantic_search (
    id integer,
    feature_type text,
    properties jsonb,
    geometry public.geometry,
    geom_type text,
    coordinates jsonb,
    search_vector tsvector,
    embedding public.vector(4096)
);


ALTER TABLE public.semantic_search OWNER TO postgres;

--
-- TOC entry 5915 (class 2604 OID 19630)
-- Name: RailwayStations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."RailwayStations" ALTER COLUMN id SET DEFAULT nextval('public."RailwayStations_id_seq"'::regclass);


--
-- TOC entry 5916 (class 2604 OID 20006)
-- Name: features id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features ALTER COLUMN id SET DEFAULT nextval('public.features_id_seq'::regclass);


--
-- TOC entry 5917 (class 2604 OID 20152)
-- Name: geo_features id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.geo_features ALTER COLUMN id SET DEFAULT nextval('public.geo_features_id_seq'::regclass);


--
-- TOC entry 5920 (class 2606 OID 19632)
-- Name: RailwayStations RailwayStations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."RailwayStations"
    ADD CONSTRAINT "RailwayStations_pkey" PRIMARY KEY (id);


--
-- TOC entry 5930 (class 2606 OID 20010)
-- Name: features features_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.features
    ADD CONSTRAINT features_pkey PRIMARY KEY (id);


--
-- TOC entry 5933 (class 2606 OID 20156)
-- Name: geo_features geo_features_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.geo_features
    ADD CONSTRAINT geo_features_pkey PRIMARY KEY (id);


--
-- TOC entry 5931 (class 1259 OID 20147)
-- Name: geo_features_search_vector_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX geo_features_search_vector_idx ON public.features USING gin (search_vector);


--
-- TOC entry 5934 (class 1259 OID 20248)
-- Name: idx_geo_features_geohash_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_geo_features_geohash_id ON public.geo_features USING btree (((properties ->> 'geohash_id'::text)));


--
-- TOC entry 5935 (class 1259 OID 20371)
-- Name: idx_geo_features_project_fts; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_geo_features_project_fts ON public.geo_features USING gin (to_tsvector('english'::regconfig, (properties ->> 'project'::text)));


--
-- TOC entry 5936 (class 1259 OID 20241)
-- Name: idx_geo_features_search_vector; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_geo_features_search_vector ON public.geo_features USING gin (search_vector);


--
-- TOC entry 5937 (class 1259 OID 20232)
-- Name: idx_geo_geom; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_geo_geom ON public.geo_features USING gist (geometry);


--
-- TOC entry 5938 (class 1259 OID 20247)
-- Name: idx_name_fts; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_name_fts ON public.geo_features USING gin (to_tsvector('english'::regconfig, (properties ->> 'name'::text)));


--
-- TOC entry 5939 (class 1259 OID 20246)
-- Name: idx_name_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_name_trgm ON public.geo_features USING gin (((properties ->> 'name'::text)) public.gin_trgm_ops);


--
-- TOC entry 5940 (class 1259 OID 20372)
-- Name: idx_project_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_project_trgm ON public.geo_features USING gin (((properties ->> 'project'::text)) public.gin_trgm_ops);


--
-- TOC entry 5921 (class 1259 OID 19834)
-- Name: idx_railwaystation_search_vector; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_railwaystation_search_vector ON public."RailwayStations" USING gin (search_vector);


--
-- TOC entry 5922 (class 1259 OID 19835)
-- Name: idx_search_vector; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_search_vector ON public."RailwayStations" USING gin (search_vector);


--
-- TOC entry 5923 (class 1259 OID 19832)
-- Name: idx_station_category_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_station_category_trgm ON public."RailwayStations" USING gin (category public.gin_trgm_ops);


--
-- TOC entry 5924 (class 1259 OID 19830)
-- Name: idx_station_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_station_location ON public."RailwayStations" USING gist (location);


--
-- TOC entry 5925 (class 1259 OID 19831)
-- Name: idx_station_name_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_station_name_trgm ON public."RailwayStations" USING gin (name public.gin_trgm_ops);


--
-- TOC entry 5926 (class 1259 OID 19833)
-- Name: idx_station_type_trgm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_station_type_trgm ON public."RailwayStations" USING gin (type public.gin_trgm_ops);


--
-- TOC entry 5941 (class 2620 OID 20146)
-- Name: features geo_features_search_vector_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER geo_features_search_vector_trigger BEFORE INSERT OR UPDATE ON public.features FOR EACH ROW EXECUTE FUNCTION public.geo_features_search_vector_update();


--
-- TOC entry 5942 (class 2620 OID 20547)
-- Name: features tsvectorupdate; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE ON public.features FOR EACH ROW EXECUTE FUNCTION public.update_search_vector();


-- Completed on 2025-05-27 12:55:56

--
-- PostgreSQL database dump complete
--


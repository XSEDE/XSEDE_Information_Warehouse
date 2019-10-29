--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: glue2; Type: SCHEMA; Schema: -; Owner: warehouse_owner
--

CREATE SCHEMA glue2;


ALTER SCHEMA glue2 OWNER TO warehouse_owner;

--
SET search_path = glue2, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: glue2_db_abstractservice; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_abstractservice (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "ServiceType" character varying(16) NOT NULL,
    "EntityJSON" text NOT NULL
);


ALTER TABLE glue2_db_abstractservice OWNER TO warehouse_owner;

--
-- Name: glue2_db_applicationenvironment; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_applicationenvironment (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" text NOT NULL
);


ALTER TABLE glue2_db_applicationenvironment OWNER TO warehouse_owner;

--
-- Name: glue2_db_applicationhandle; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_applicationhandle (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" text NOT NULL,
    "ApplicationEnvironmentID_id" character varying(64) NOT NULL
);


ALTER TABLE glue2_db_applicationhandle OWNER TO warehouse_owner;

--
-- Name: glue2_db_computingactivity; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_computingactivity (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" text NOT NULL
);


ALTER TABLE glue2_db_computingactivity OWNER TO warehouse_owner;

--
-- Name: glue2_db_computingmanager; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_computingmanager (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" text NOT NULL
);


ALTER TABLE glue2_db_computingmanager OWNER TO warehouse_owner;

--
-- Name: glue2_db_computingshare; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_computingshare (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" text NOT NULL
);


ALTER TABLE glue2_db_computingshare OWNER TO warehouse_owner;

--
-- Name: glue2_db_endpoint; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_endpoint (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" text NOT NULL,
    "AbstractServiceID_id" character varying(64) NOT NULL
);


ALTER TABLE glue2_db_endpoint OWNER TO warehouse_owner;

--
-- Name: glue2_db_entityhistory; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_entityhistory (
    id integer NOT NULL,
    "Exchange" character varying(32) NOT NULL,
    "RoutingKey" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "MessageJSON" text NOT NULL
);


ALTER TABLE glue2_db_entityhistory OWNER TO warehouse_owner;

--
-- Name: glue2_db_entityhistory_id_seq; Type: SEQUENCE; Schema: glue2; Owner: warehouse_owner
--

CREATE SEQUENCE glue2_db_entityhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE glue2_db_entityhistory_id_seq OWNER TO warehouse_owner;

--
-- Name: glue2_db_entityhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: glue2; Owner: warehouse_owner
--

ALTER SEQUENCE glue2_db_entityhistory_id_seq OWNED BY glue2_db_entityhistory.id;


--
-- Name: glue2_db_executionenvironment; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_executionenvironment (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" text NOT NULL
);


ALTER TABLE glue2_db_executionenvironment OWNER TO warehouse_owner;

--
-- Name: glue2_db_location; Type: TABLE; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE TABLE glue2_db_location (
    "ID" character varying(64) NOT NULL,
    "ResourceID" character varying(32) NOT NULL,
    "Name" character varying(32) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" text NOT NULL
);


ALTER TABLE glue2_db_location OWNER TO warehouse_owner;

--
-- Name: id; Type: DEFAULT; Schema: glue2; Owner: warehouse_owner
--

ALTER TABLE ONLY glue2_db_entityhistory ALTER COLUMN id SET DEFAULT nextval('glue2_db_entityhistory_id_seq'::regclass);


--
-- Name: glue2_db_abstractservice_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_abstractservice
    ADD CONSTRAINT glue2_db_abstractservice_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_applicationenvironment_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_applicationenvironment
    ADD CONSTRAINT glue2_db_applicationenvironment_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_applicationhandle_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_applicationhandle
    ADD CONSTRAINT glue2_db_applicationhandle_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_computingactivity_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_computingactivity
    ADD CONSTRAINT glue2_db_computingactivity_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_computingmanager_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_computingmanager
    ADD CONSTRAINT glue2_db_computingmanager_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_computingshare_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_computingshare
    ADD CONSTRAINT glue2_db_computingshare_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_endpoint_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_endpoint
    ADD CONSTRAINT glue2_db_endpoint_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_entityhistory_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_entityhistory
    ADD CONSTRAINT glue2_db_entityhistory_pkey PRIMARY KEY (id);


--
-- Name: glue2_db_executionenvironment_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_executionenvironment
    ADD CONSTRAINT glue2_db_executionenvironment_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_location_pkey; Type: CONSTRAINT; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_location
    ADD CONSTRAINT glue2_db_location_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_abstractservice_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_abstractservice_4bf17acd ON glue2_db_abstractservice USING btree ("ResourceID");


--
-- Name: glue2_db_applicationenvironment_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_applicationenvironment_4bf17acd ON glue2_db_applicationenvironment USING btree ("ResourceID");


--
-- Name: glue2_db_applicationhandle_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_applicationhandle_4bf17acd ON glue2_db_applicationhandle USING btree ("ResourceID");


--
-- Name: glue2_db_applicationhandle_bd82b482; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_applicationhandle_bd82b482 ON glue2_db_applicationhandle USING btree ("ApplicationEnvironmentID_id");


--
-- Name: glue2_db_computingactivity_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_computingactivity_4bf17acd ON glue2_db_computingactivity USING btree ("ResourceID");


--
-- Name: glue2_db_computingmanager_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_computingmanager_4bf17acd ON glue2_db_computingmanager USING btree ("ResourceID");


--
-- Name: glue2_db_computingshare_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_computingshare_4bf17acd ON glue2_db_computingshare USING btree ("ResourceID");


--
-- Name: glue2_db_endpoint_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_endpoint_4bf17acd ON glue2_db_endpoint USING btree ("ResourceID");


--
-- Name: glue2_db_endpoint_6ba651aa; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_endpoint_6ba651aa ON glue2_db_endpoint USING btree ("AbstractServiceID_id");


--
-- Name: glue2_db_entityhistory_992374d8; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_entityhistory_992374d8 ON glue2_db_entityhistory USING btree ("Exchange");


--
-- Name: glue2_db_entityhistory_e67813fa; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_entityhistory_e67813fa ON glue2_db_entityhistory USING btree ("RoutingKey");


--
-- Name: glue2_db_executionenvironment_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_executionenvironment_4bf17acd ON glue2_db_executionenvironment USING btree ("ResourceID");


--
-- Name: glue2_db_location_4bf17acd; Type: INDEX; Schema: glue2; Owner: warehouse_owner; Tablespace: 
--

CREATE INDEX glue2_db_location_4bf17acd ON glue2_db_location USING btree ("ResourceID");


--
-- Name: D5bb83a32eccb06a38a1d83db0308c4d; Type: FK CONSTRAINT; Schema: glue2; Owner: warehouse_owner
--

ALTER TABLE ONLY glue2_db_applicationhandle
    ADD CONSTRAINT "D5bb83a32eccb06a38a1d83db0308c4d" FOREIGN KEY ("ApplicationEnvironmentID_id") REFERENCES glue2_db_applicationenvironment("ID") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D9e1631737227a3f8786c834236050b7; Type: FK CONSTRAINT; Schema: glue2; Owner: warehouse_owner
--

ALTER TABLE ONLY glue2_db_endpoint
    ADD CONSTRAINT "D9e1631737227a3f8786c834236050b7" FOREIGN KEY ("AbstractServiceID_id") REFERENCES glue2_db_abstractservice("ID") DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--


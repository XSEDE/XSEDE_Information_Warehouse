--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = glue2, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: django_migrations; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO glue2_owner;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: glue2; Owner: glue2_owner
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO glue2_owner;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: glue2; Owner: glue2_owner
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: glue2_db_abstractservice; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_abstractservice (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL,
    "ServiceType" character varying(16) NOT NULL
);


ALTER TABLE glue2_db_abstractservice OWNER TO glue2_owner;

--
-- Name: glue2_db_applicationenvironment; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_applicationenvironment (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL
);


ALTER TABLE glue2_db_applicationenvironment OWNER TO glue2_owner;

--
-- Name: glue2_db_applicationhandle; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_applicationhandle (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL,
    "ApplicationEnvironmentID_id" character varying(120)
);


ALTER TABLE glue2_db_applicationhandle OWNER TO glue2_owner;

--
-- Name: glue2_db_computingactivity; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_computingactivity (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL
);


ALTER TABLE glue2_db_computingactivity OWNER TO glue2_owner;

--
-- Name: glue2_db_computingmanager; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_computingmanager (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL
);


ALTER TABLE glue2_db_computingmanager OWNER TO glue2_owner;

--
-- Name: glue2_db_computingshare; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_computingshare (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL
);


ALTER TABLE glue2_db_computingshare OWNER TO glue2_owner;

--
-- Name: glue2_db_endpoint; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_endpoint (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL,
    "AbstractServiceID_id" character varying(120) NOT NULL
);


ALTER TABLE glue2_db_endpoint OWNER TO glue2_owner;

--
-- Name: glue2_db_entityhistory; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_entityhistory (
    "ID" integer NOT NULL,
    "DocumentType" character varying(32) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "ReceivedTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL
);


ALTER TABLE glue2_db_entityhistory OWNER TO glue2_owner;

--
-- Name: glue2_db_entityhistory_ID_seq; Type: SEQUENCE; Schema: glue2; Owner: glue2_owner
--

CREATE SEQUENCE "glue2_db_entityhistory_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "glue2_db_entityhistory_ID_seq" OWNER TO glue2_owner;

--
-- Name: glue2_db_entityhistory_ID_seq; Type: SEQUENCE OWNED BY; Schema: glue2; Owner: glue2_owner
--

ALTER SEQUENCE "glue2_db_entityhistory_ID_seq" OWNED BY glue2_db_entityhistory."ID";


--
-- Name: glue2_db_executionenvironment; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_executionenvironment (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL
);


ALTER TABLE glue2_db_executionenvironment OWNER TO glue2_owner;

--
-- Name: glue2_db_location; Type: TABLE; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE TABLE glue2_db_location (
    "ID" character varying(120) NOT NULL,
    "ResourceID" character varying(40) NOT NULL,
    "Name" character varying(96) NOT NULL,
    "CreationTime" timestamp with time zone NOT NULL,
    "EntityJSON" jsonb NOT NULL
);


ALTER TABLE glue2_db_location OWNER TO glue2_owner;

--
-- Name: id; Type: DEFAULT; Schema: glue2; Owner: glue2_owner
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: ID; Type: DEFAULT; Schema: glue2; Owner: glue2_owner
--

ALTER TABLE ONLY glue2_db_entityhistory ALTER COLUMN "ID" SET DEFAULT nextval('"glue2_db_entityhistory_ID_seq"'::regclass);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: glue2_db_abstractservice_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_abstractservice
    ADD CONSTRAINT glue2_db_abstractservice_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_applicationenvironment_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_applicationenvironment
    ADD CONSTRAINT glue2_db_applicationenvironment_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_applicationhandle_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_applicationhandle
    ADD CONSTRAINT glue2_db_applicationhandle_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_computingactivity_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_computingactivity
    ADD CONSTRAINT glue2_db_computingactivity_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_computingmanager_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_computingmanager
    ADD CONSTRAINT glue2_db_computingmanager_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_computingshare_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_computingshare
    ADD CONSTRAINT glue2_db_computingshare_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_endpoint_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_endpoint
    ADD CONSTRAINT glue2_db_endpoint_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_entityhistory_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_entityhistory
    ADD CONSTRAINT glue2_db_entityhistory_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_executionenvironment_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_executionenvironment
    ADD CONSTRAINT glue2_db_executionenvironment_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_location_pkey; Type: CONSTRAINT; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

ALTER TABLE ONLY glue2_db_location
    ADD CONSTRAINT glue2_db_location_pkey PRIMARY KEY ("ID");


--
-- Name: glue2_db_abstractservice_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_abstractservice_4bf17acd ON glue2_db_abstractservice USING btree ("ResourceID");


--
-- Name: glue2_db_abstractservice_ID_6286021c00faa96_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_abstractservice_ID_6286021c00faa96_like" ON glue2_db_abstractservice USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_abstractservice_ResourceID_41cb2c7d81e48e6e_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_abstractservice_ResourceID_41cb2c7d81e48e6e_like" ON glue2_db_abstractservice USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_appl_ApplicationEnvironmentID_id_7372c3c787971c59_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_appl_ApplicationEnvironmentID_id_7372c3c787971c59_like" ON glue2_db_applicationhandle USING btree ("ApplicationEnvironmentID_id" varchar_pattern_ops);


--
-- Name: glue2_db_applicationenvironmen_ResourceID_7ad9eff81aff1487_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_applicationenvironmen_ResourceID_7ad9eff81aff1487_like" ON glue2_db_applicationenvironment USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_applicationenvironment_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_applicationenvironment_4bf17acd ON glue2_db_applicationenvironment USING btree ("ResourceID");


--
-- Name: glue2_db_applicationenvironment_ID_5a033d455bdab58b_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_applicationenvironment_ID_5a033d455bdab58b_like" ON glue2_db_applicationenvironment USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_applicationhandle_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_applicationhandle_4bf17acd ON glue2_db_applicationhandle USING btree ("ResourceID");


--
-- Name: glue2_db_applicationhandle_ID_5f3b32ff927b3e5d_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_applicationhandle_ID_5f3b32ff927b3e5d_like" ON glue2_db_applicationhandle USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_applicationhandle_ResourceID_74dbdb90502cc2a7_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_applicationhandle_ResourceID_74dbdb90502cc2a7_like" ON glue2_db_applicationhandle USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_applicationhandle_bd82b482; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_applicationhandle_bd82b482 ON glue2_db_applicationhandle USING btree ("ApplicationEnvironmentID_id");


--
-- Name: glue2_db_computingactivity_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_computingactivity_4bf17acd ON glue2_db_computingactivity USING btree ("ResourceID");


--
-- Name: glue2_db_computingactivity_ID_7083bab308cbaf32_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_computingactivity_ID_7083bab308cbaf32_like" ON glue2_db_computingactivity USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_computingactivity_ResourceID_6a80b6bf3eb137ca_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_computingactivity_ResourceID_6a80b6bf3eb137ca_like" ON glue2_db_computingactivity USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_computingmanager_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_computingmanager_4bf17acd ON glue2_db_computingmanager USING btree ("ResourceID");


--
-- Name: glue2_db_computingmanager_ID_5835a522f0940d89_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_computingmanager_ID_5835a522f0940d89_like" ON glue2_db_computingmanager USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_computingmanager_ResourceID_4aaf1553f528765b_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_computingmanager_ResourceID_4aaf1553f528765b_like" ON glue2_db_computingmanager USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_computingshare_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_computingshare_4bf17acd ON glue2_db_computingshare USING btree ("ResourceID");


--
-- Name: glue2_db_computingshare_ID_5dfea64c60dd7b47_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_computingshare_ID_5dfea64c60dd7b47_like" ON glue2_db_computingshare USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_computingshare_ResourceID_69cf6e64ac3a2a43_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_computingshare_ResourceID_69cf6e64ac3a2a43_like" ON glue2_db_computingshare USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_endpoint_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_endpoint_4bf17acd ON glue2_db_endpoint USING btree ("ResourceID");


--
-- Name: glue2_db_endpoint_6ba651aa; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_endpoint_6ba651aa ON glue2_db_endpoint USING btree ("AbstractServiceID_id");


--
-- Name: glue2_db_endpoint_AbstractServiceID_id_564f907f7fc28dee_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_endpoint_AbstractServiceID_id_564f907f7fc28dee_like" ON glue2_db_endpoint USING btree ("AbstractServiceID_id" varchar_pattern_ops);


--
-- Name: glue2_db_endpoint_ID_3160a1bbbc3f1199_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_endpoint_ID_3160a1bbbc3f1199_like" ON glue2_db_endpoint USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_endpoint_ResourceID_415928348f722895_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_endpoint_ResourceID_415928348f722895_like" ON glue2_db_endpoint USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_entityhistory_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_entityhistory_4bf17acd ON glue2_db_entityhistory USING btree ("ResourceID");


--
-- Name: glue2_db_entityhistory_DocumentType_4b6ce6ab99b8d3be_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_entityhistory_DocumentType_4b6ce6ab99b8d3be_like" ON glue2_db_entityhistory USING btree ("DocumentType" varchar_pattern_ops);


--
-- Name: glue2_db_entityhistory_ResourceID_7c8fc32feef9f474_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_entityhistory_ResourceID_7c8fc32feef9f474_like" ON glue2_db_entityhistory USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_entityhistory_a3e4a918; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_entityhistory_a3e4a918 ON glue2_db_entityhistory USING btree ("DocumentType");


--
-- Name: glue2_db_executionenvironment_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_executionenvironment_4bf17acd ON glue2_db_executionenvironment USING btree ("ResourceID");


--
-- Name: glue2_db_executionenvironment_ID_3eb8178d6c5c3f3d_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_executionenvironment_ID_3eb8178d6c5c3f3d_like" ON glue2_db_executionenvironment USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_executionenvironment_ResourceID_29ee490ce0ad2639_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_executionenvironment_ResourceID_29ee490ce0ad2639_like" ON glue2_db_executionenvironment USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: glue2_db_location_4bf17acd; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX glue2_db_location_4bf17acd ON glue2_db_location USING btree ("ResourceID");


--
-- Name: glue2_db_location_ID_43d2b5fdbe2be9fb_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_location_ID_43d2b5fdbe2be9fb_like" ON glue2_db_location USING btree ("ID" varchar_pattern_ops);


--
-- Name: glue2_db_location_ResourceID_63383f6e74b6397f_like; Type: INDEX; Schema: glue2; Owner: glue2_owner; Tablespace: 
--

CREATE INDEX "glue2_db_location_ResourceID_63383f6e74b6397f_like" ON glue2_db_location USING btree ("ResourceID" varchar_pattern_ops);


--
-- Name: D5bb83a32eccb06a38a1d83db0308c4d; Type: FK CONSTRAINT; Schema: glue2; Owner: glue2_owner
--

ALTER TABLE ONLY glue2_db_applicationhandle
    ADD CONSTRAINT "D5bb83a32eccb06a38a1d83db0308c4d" FOREIGN KEY ("ApplicationEnvironmentID_id") REFERENCES glue2_db_applicationenvironment("ID") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D9e1631737227a3f8786c834236050b7; Type: FK CONSTRAINT; Schema: glue2; Owner: glue2_owner
--

ALTER TABLE ONLY glue2_db_endpoint
    ADD CONSTRAINT "D9e1631737227a3f8786c834236050b7" FOREIGN KEY ("AbstractServiceID_id") REFERENCES glue2_db_abstractservice("ID") DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--


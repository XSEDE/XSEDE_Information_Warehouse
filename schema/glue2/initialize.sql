--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE django_owner;
ALTER ROLE django_owner WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION PASSWORD 'md50241916e563ec8b68a2de0a6be0af1a3';
ALTER ROLE django_owner SET search_path TO django;

CREATE ROLE glue2_owner;
ALTER ROLE glue2_owner WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION PASSWORD 'md54ca2fe9bca416d248039cb5c35b76b54';
ALTER ROLE glue2_owner SET search_path TO glue2;

CREATE ROLE xcsr_owner;
ALTER ROLE xcsr_owner WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION PASSWORD 'md54ca2fe9bca416d248039cb5c35b76b54';
ALTER ROLE xcsr_owner SET search_path TO xcsr;

ALTER ROLE warehouse_owner SET search_path TO glue2;


--
-- Database and Schemas
--
CREATE DATABASE warehouse;
ALTER DATABASE warehouse OWNER TO warehouse_owner;
\c warehouse

CREATE SCHEMA django;
ALTER SCHEMA django OWNER TO django_owner;

CREATE SCHEMA glue2;
ALTER SCHEMA glue2 OWNER TO glue2_owner;

CREATE SCHEMA xcsr;
ALTER SCHEMA xcsr OWNER TO xcsr_owner;


--
-- Loader
--
CREATE role warehouse_load nosuperuser login password 'xxx';
GRANT select,insert,update,delete ON ALL TABLES IN SCHEMA glue2 TO warehouse_load;
ALTER ROLE warehouse_load SET client_encodING = 'UTF8';
ALTER ROLE warehouse_load SET default_transaction_isolation = 'read committed';
ALTER ROLE warehouse_load SET timezone = 'UTC';

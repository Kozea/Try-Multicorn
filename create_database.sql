-- Create and switch to the database
CREATE database multicorn;
CREATE user multicorn_admin;
CREATE user multicorn;

\connect multicorn;

-- Setup extension
create extension multicorn;
create server multicorn_srv foreign data wrapper multicorn;
grant usage on foreign server multicorn_srv to multicorn_admin;


-- Create necessary roles
CREATE role restricted;
grant restricted to multicorn_admin;
grant restricted to multicorn;
REVOKE all privileges on all databases from restricted;
REVOKE all privileges on all tables in schema pg_catalog from public;
REVOKE all privileges on schema public from public;
REVOKE all privileges on schema information_schema from public;
-- Admin must know if tables exists
GRANT select on pg_class to multicorn_admin;
GRANT select on pg_namespace to multicorn_admin;

-- REVOKE all privileges on function PG_SLEEP(numeric) from public;

GRANT connect on database multicorn to multicorn_admin;
GRANT connect on database multicorn to multicorn;

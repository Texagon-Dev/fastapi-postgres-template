-- Create the 'cipher' role if it does not exist
DO
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'hbky') THEN
        CREATE ROLE hbky WITH LOGIN;
        ALTER ROLE hbky WITH PASSWORD 'password';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE fastapi_db TO hbky;
ALTER SCHEMA public OWNER TO hbky;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hbky;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hbky;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO hbky;
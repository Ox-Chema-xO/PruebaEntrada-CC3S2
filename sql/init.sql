-- Script de inicialización para la base de datos 
\i /docker-entrypoint-initdb.d/schema.sql

\i /docker-entrypoint-initdb.d/seed.sql

ALTER DATABASE trivia_db SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE trivia_db TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

\echo 'Inicialización de la base de datos trivia_db completada con éxito.'
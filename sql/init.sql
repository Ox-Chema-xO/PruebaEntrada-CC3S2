-- Script de inicialización para la base de datos de Trivia Quiz
-- Este archivo ejecuta los scripts de esquema y datos iniciales

-- Crear esquema de la base de datos
\i /docker-entrypoint-initdb.d/schema.sql

-- Cargar datos iniciales
\i /docker-entrypoint-initdb.d/seed.sql

-- Configuraciones adicionales
ALTER DATABASE trivia_db SET timezone TO 'UTC';

-- Otorgar privilegios
GRANT ALL PRIVILEGES ON DATABASE trivia_db TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Mensaje de finalización
\echo 'Inicialización de la base de datos trivia_db completada con éxito.'
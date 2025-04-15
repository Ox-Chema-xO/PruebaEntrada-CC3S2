-- Esquema para la base de datos de Trivia Quiz

-- Eliminamos tablas si existen para evitar conflictos
DROP TABLE IF EXISTS quiz_questions CASCADE;
DROP TABLE IF EXISTS quizzes CASCADE;
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS difficulty_levels CASCADE;

-- Tabla para niveles de dificultad
CREATE TABLE difficulty_levels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Tabla para almacenar las preguntas
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    options TEXT[] NOT NULL,
    correct_answer TEXT NOT NULL,
    difficulty_id INTEGER REFERENCES difficulty_levels(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para almacenar quizzes
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    total_questions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    incorrect_answers INTEGER DEFAULT 0,
    current_difficulty_id INTEGER REFERENCES difficulty_levels(id),
    consecutive_correct INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Tabla de relación entre quizzes y preguntas
CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes(id) ON DELETE CASCADE,
    question_id INTEGER REFERENCES questions(id),
    user_answer TEXT,
    is_correct BOOLEAN,
    answered_at TIMESTAMP,
    question_index INTEGER NOT NULL
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_questions_difficulty_id ON questions(difficulty_id);
CREATE INDEX idx_quizzes_difficulty_id ON quizzes(current_difficulty_id);
CREATE INDEX idx_quiz_questions_quiz_id ON quiz_questions(quiz_id);
-- Datos iniciales para la base de datos de Trivia Quiz

-- Insertamos los niveles de dificultad
INSERT INTO difficulty_levels (name, description) VALUES 
    ('fácil', 'Preguntas de conocimiento general básico'),
    ('normal', 'Preguntas de dificultad media'),
    ('difícil', 'Preguntas avanzadas y específicas');

-- Insertamos las preguntas de dificultad fácil
INSERT INTO questions (description, options, correct_answer, difficulty_id) VALUES
    ('¿Cuál es la capital de Francia?', 
     ARRAY['Madrid', 'Londres', 'París', 'Berlín'], 
     'París', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),
    
    ('¿Cuál es el océano más grande del mundo?', 
     ARRAY['Atlántico', 'Pacífico', 'Índico', 'Ártico'], 
     'Pacífico', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),
    
    ('¿Quién pintó La Mona Lisa?', 
     ARRAY['Miguel Ángel', 'Leonardo da Vinci', 'Pablo Picasso', 'Vincent van Gogh'], 
     'Leonardo da Vinci', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),
    
    ('¿Cuál es la montaña más alta del mundo?', 
     ARRAY['Monte Everest', 'K2', 'Monte Kilimanjaro', 'Monte McKinley'], 
     'Monte Everest', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),
    
    ('¿Qué científico propuso la teoría de la relatividad?', 
     ARRAY['Isaac Newton', 'Albert Einstein', 'Niels Bohr', 'Galileo Galilei'], 
     'Albert Einstein', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil'));

-- Insertamos las preguntas de dificultad normal
INSERT INTO questions (description, options, correct_answer, difficulty_id) VALUES
    ('¿Quién escribió "Don Quijote de la Mancha"?', 
     ARRAY['Gabriel García Márquez', 'Miguel de Cervantes', 'Jorge Luis Borges', 'Federico García Lorca'], 
     'Miguel de Cervantes', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),
    
    ('¿Cuál es el río más largo del mundo?', 
     ARRAY['Nilo', 'Amazonas', 'Misisipi', 'Yangtze'], 
     'Amazonas', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),
    
    ('¿En qué año comenzó la Segunda Guerra Mundial?', 
     ARRAY['1939', '1940', '1941', '1945'], 
     '1939', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),
    
    ('¿Cuál es el planeta más grande del Sistema Solar?', 
     ARRAY['Tierra', 'Júpiter', 'Saturno', 'Neptuno'], 
     'Júpiter', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),
    
    ('¿Qué país tiene la mayor población del mundo?', 
     ARRAY['India', 'Estados Unidos', 'China', 'Indonesia'], 
     'China', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),
    
    ('¿Cuál es el símbolo químico del oro?', 
     ARRAY['Au', 'Ag', 'Fe', 'Cu'], 
     'Au', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),
    
    ('¿Cuál es el hueso más largo del cuerpo humano?', 
     ARRAY['Fémur', 'Húmero', 'Tibia', 'Radio'], 
     'Fémur', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal'));

-- Insertamos las preguntas de dificultad difícil
INSERT INTO questions (description, options, correct_answer, difficulty_id) VALUES
    ('¿Cuál es el elemento químico más abundante en la corteza terrestre?', 
     ARRAY['Hierro', 'Oxígeno', 'Silicio', 'Aluminio'], 
     'Oxígeno', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),
    
    ('¿Cuál es la velocidad de la luz en el vacío?', 
     ARRAY['300,000 km/s', '150,000 km/s', '200,000 km/s', '250,000 km/s'], 
     '300,000 km/s', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),
    
    ('¿En qué año se fundó la ONU?', 
     ARRAY['1945', '1950', '1939', '1955'], 
     '1945', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil'));
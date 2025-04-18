INSERT INTO difficulty_levels (name, description) VALUES 
    ('fácil', 'Preguntas de conocimiento general básico'),
    ('normal', 'Preguntas de dificultad media'),
    ('difícil', 'Preguntas avanzadas y específicas');

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
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),
    
    ('¿En qué continente se encuentra Egipto?', 
     ARRAY['Asia', 'África', 'Europa', 'Oceanía'], 
     'África', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),

    ('¿Cuál es el animal terrestre más grande?', 
     ARRAY['Elefante', 'Rinoceronte', 'Jirafa', 'Oso polar'], 
     'Elefante', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),

    ('¿En qué ciudad se encuentra la Torre Eiffel?', 
     ARRAY['Roma', 'Londres', 'París', 'Madrid'], 
     'París', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),

    ('¿Cuál es el continente más grande del mundo?', 
     ARRAY['Asia', 'América', 'África', 'Europa'], 
     'Asia', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil')),

    ('¿Qué país tiene la mayor cantidad de pirámides?', 
     ARRAY['Egipto', 'México', 'Sudán', 'Perú'], 
     'Sudán', 
     (SELECT id FROM difficulty_levels WHERE name = 'fácil'));


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
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),
    
    ('¿Qué continente tiene más países?', 
     ARRAY['África', 'Asia', 'Europa', 'América'], 
     'África', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),

    ('¿Qué escritor famoso de los siguiente, nació en Argentina?', 
     ARRAY['Pablo Neruda', 'Gabriel García Márquez', 'Jorge Luis Borges', 'Mario Vargas Llosa'], 
     'Jorge Luis Borges', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal')),

    ('¿Cuál es la capital de Canadá?', 
     ARRAY['Vancouver', 'Toronto', 'Ottawa', 'Montreal'], 
     'Ottawa', 
     (SELECT id FROM difficulty_levels WHERE name = 'normal'));


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
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),

    ('¿Qué teoría desarrolló Albert Einstein sobre la gravitación?', 
     ARRAY['Teoría de la relatividad especial', 'Teoría de la relatividad general', 'Teoría cuántica', 'Teoría de cuerdas'], 
     'Teoría de la relatividad general', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),

    ('¿Quién desarrolló la teoría de la evolución por selección natural?', 
     ARRAY['Charles Darwin', 'Gregor Mendel', 'Niels Bohr', 'Louis Pasteur'], 
     'Charles Darwin', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),

    ('¿Cuál es el nombre del primer satélite artificial lanzado por la humanidad?', 
     ARRAY['Sputnik 1', 'Apollo 11', 'Voyager 1', 'Hubble'], 
     'Sputnik 1', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),

    ('¿Qué matemático es conocido por su teorema sobre los triángulos rectángulos?', 
     ARRAY['Pitagoras', 'Arquímedes', 'Euclides', 'Descartes'], 
     'Pitagoras', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),

    ('¿Qué físico propuso el principio de incertidumbre en la mecánica cuántica?', 
     ARRAY['Niels Bohr', 'Max Planck', 'Werner Heisenberg', 'Albert Einstein'], 
     'Werner Heisenberg', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),

    ('¿Cuál es la teoría que describe el comportamiento de las partículas subatómicas?', 
     ARRAY['Teoría cuántica', 'Teoría relativista', 'Teoría del caos', 'Teoría de cuerdas'], 
     'Teoría cuántica', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil')),

    ('¿Cuál es la última capa de la atmósfera terrestre?', 
     ARRAY['Estratósfera', 'Termósfera', 'Exósfera', 'Mesósfera'], 
     'Exósfera', 
     (SELECT id FROM difficulty_levels WHERE name = 'difícil'));

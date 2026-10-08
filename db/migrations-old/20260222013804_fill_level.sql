-- migrate:up

INSERT INTO levels (id, name) VALUES
(1, 'Inicial 3 años'),
(2, 'Inicial 4 años'),
(3, 'Inicial 5 años'),

(4, '1° Primaria'),
(5, '2° Primaria'),
(6, '3° Primaria'),
(7, '4° Primaria'),
(8, '5° Primaria'),
(9, '6° Primaria'),

(10, '1° Secundaria'),
(11, '2° Secundaria'),
(12, '3° Secundaria'),
(13, '4° Secundaria'),
(14, '5° Secundaria'),

(15, 'Talleres de Arte'),
(16, 'Talleres de Deporte'),
(17, 'Círculos de Estudio');

-- migrate:down

DELETE FROM levels;
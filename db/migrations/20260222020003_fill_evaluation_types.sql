-- migrate:up

INSERT INTO evaluation_types (id, name) VALUES
(1, 'Evaluación Diagnóstica'),
(2, 'Evaluación Formativa'),
(3, 'Evaluación Sumativa'),
(4, 'Práctica Calificada'),
(5, 'Examen Parcial'),
(6, 'Examen Final'),
(7, 'Trabajo Individual'),
(8, 'Trabajo Grupal'),
(9, 'Exposición'),
(10, 'Proyecto'),
(11, 'Tarea'),
(12, 'Participación en Clase'),
(13, 'Control de Lectura'),
(14, 'Autoevaluación'),
(15, 'Coevaluación');

-- migrate:down

DELETE FROM evaluation_types;
-- migrate:up

INSERT INTO course_branches (id, name) VALUES
(1, 'Matemáticas'),
(2, 'Ciencias Sociales'),
(3, 'Letras'),
(4, 'Arte'),
(5, 'Deportes'),
(6, 'Talleres');

-- migrate:down

DELETE FROM course_branches;
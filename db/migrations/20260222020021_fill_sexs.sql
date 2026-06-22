-- migrate:up

INSERT INTO sexs (id, name) VALUES
(1, 'Masculino'),
(2, 'Femenino'),
(3, 'No especificado');

-- migrate:down

DELETE FROM sexs;
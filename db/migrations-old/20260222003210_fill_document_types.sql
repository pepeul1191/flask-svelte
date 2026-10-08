-- migrate:up

INSERT INTO document_types (id, name) VALUES
(1, 'DNI'),
(2, 'Carné Extranjería'),
(3, 'Pasaporte');

-- migrate:down

DELETE FROM document_types;
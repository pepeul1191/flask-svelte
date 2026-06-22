-- migrate:up

INSERT INTO departments (id, name) VALUES (1, 'Amazonas');
INSERT INTO departments (id, name) VALUES (2, 'Ancash');
INSERT INTO departments (id, name) VALUES (3, 'Apurimac');
INSERT INTO departments (id, name) VALUES (4, 'Arequipa');
INSERT INTO departments (id, name) VALUES (5, 'Ayacucho');
INSERT INTO departments (id, name) VALUES (6, 'Cajamarca');
INSERT INTO departments (id, name) VALUES (7, 'Callao');
INSERT INTO departments (id, name) VALUES (8, 'Cuzco');
INSERT INTO departments (id, name) VALUES (9, 'Huancavelica');
INSERT INTO departments (id, name) VALUES (10, 'Huánuco');
INSERT INTO departments (id, name) VALUES (11, 'Ica');
INSERT INTO departments (id, name) VALUES (12, 'Junin');
INSERT INTO departments (id, name) VALUES (13, 'La Libertad');
INSERT INTO departments (id, name) VALUES (14, 'Lambayeque');
INSERT INTO departments (id, name) VALUES (15, 'Lima');
INSERT INTO departments (id, name) VALUES (16, 'Loreto');
INSERT INTO departments (id, name) VALUES (17, 'Madre de Dios');
INSERT INTO departments (id, name) VALUES (18, 'Moquegua');
INSERT INTO departments (id, name) VALUES (19, 'Pasco');
INSERT INTO departments (id, name) VALUES (20, 'Piura');
INSERT INTO departments (id, name) VALUES (21, 'Puno');
INSERT INTO departments (id, name) VALUES (22, 'San Martín');
INSERT INTO departments (id, name) VALUES (23, 'Tacna');
INSERT INTO departments (id, name) VALUES (24, 'Tumbes');
INSERT INTO departments (id, name) VALUES (25, 'Ucayali');

-- migrate:down

DELETE FROM departments
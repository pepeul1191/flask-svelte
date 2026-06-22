-- migrate:up

INSERT INTO representative_roles (id, name) VALUES (1, 'Padre');
INSERT INTO representative_roles (id, name) VALUES (2, 'Madre');
INSERT INTO representative_roles (id, name) VALUES (3, 'Abuelo');
INSERT INTO representative_roles (id, name) VALUES (4, 'Abuela');
INSERT INTO representative_roles (id, name) VALUES (5, 'Tío');
INSERT INTO representative_roles (id, name) VALUES (6, 'Tía');
INSERT INTO representative_roles (id, name) VALUES (7, 'Hermano');
INSERT INTO representative_roles (id, name) VALUES (8, 'Hermana');
INSERT INTO representative_roles (id, name) VALUES (9, 'Apoderado');

-- migrate:down

DELETE FROM representative_roles
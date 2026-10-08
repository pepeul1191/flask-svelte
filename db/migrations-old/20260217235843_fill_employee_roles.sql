-- migrate:up

INSERT INTO employee_roles (id, name) VALUES (1, 'Coordinador');
INSERT INTO employee_roles (id, name) VALUES (2, 'Profesor');
INSERT INTO employee_roles (id, name) VALUES (3, 'Tutor');
INSERT INTO employee_roles (id, name) VALUES (4, 'Auxiliar');

-- migrate:down

DELETE FROM employee_roles
-- migrate:up

INSERT INTO clients (id, name, contact_name, email, phone, address, notes) VALUES
(1, 'Industrias Alimentarias S.A.C.', 'Carlos Mendoza', 'contacto@industriasalimentarias.pe', '+51987654321', 'Av. Argentina 1234, Callao', 'Cliente preferencial del sector industrial de alimentos.'),
(2, 'Minera Los Andes S.A.', 'María Fernández', 'mfernandez@losandesminera.com', '+51912345678', 'Calle Las Begonias 456, San Isidro, Lima', 'Requiere mantenimiento preventivo trimestral.');

-- migrate:down

DELETE FROM clients;
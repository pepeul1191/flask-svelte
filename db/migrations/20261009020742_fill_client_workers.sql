-- migrate:up

INSERT INTO client_workers (id, client_id, user_id, names, last_names, email, document, phone, certification, position) VALUES
(1, 1, NULL, 'Roberto Carlos', 'Silva Pérez', 'rsilva@industriasalimentarias.pe', '45678912', '+51987111222', 'ISO 9001 Auditor Interno', 'Jefe de Mantenimiento'),
(2, 1, NULL, 'Ana Sofía', 'Torres Rivas', 'atorres@industriasalimentarias.pe', '47891234', '+51987333444', 'Técnico Electromecánico Avanzado', 'Supervisora de Línea'),
(3, 1, NULL, 'Jorge Luis', 'Paredes Castro', 'jparedes@system.local', '42123456', '+51987555666', 'Soldadura Homologada 6G', 'Técnico Soldador'),
(4, 1, NULL, 'Carmen Rosa', 'Vásquez Huamán', 'cvasquez@system.local', '48901234', '+51987777888', 'Seguridad Industrial OHSAS', 'Especialista EHS'),
(5, 2, NULL, 'Luis Alberto', 'Espinoza Rojas', 'lespinoza@losandesminera.com', '40123456', '+51912111222', 'Certificación CAT Maquinaria Pesada', 'Mecánico de Planta Senior'),
(6, 2, NULL, 'Rosa Elena', 'Chávez Medina', 'rchavez@losandesminera.com', '43456789', '+51912333444', 'Especialista en Automatización PLC', 'Ingeniera de Control'),
(7, 2, NULL, 'Manuel Ángel', 'Ramos Quispe', 'mramos@system.local', '46789012', '+51912555666', 'Técnico en Hidráulica Industrial', 'Asistente de Mantenimiento');

-- migrate:down

DELETE FROM client_workers;
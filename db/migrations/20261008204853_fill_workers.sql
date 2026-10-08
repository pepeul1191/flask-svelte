-- migrate:up

INSERT INTO workers (id, user_id, names, last_names, email, document, phone, certification, position, created_at, updated_at) VALUES
(1, NULL, 'Carlos Alberto', 'Gutiérrez Mendoza', 'carlos.gutierrez@system.local', '45879632', '+51987654321', 'ISO 18436-2 Categoria II (Vibraciones)', 'Técnico de Confiabilidad', NOW(), NOW()),
(2, NULL, 'Juan Carlos', 'Pérez Silva', 'juan.perez@system.local', '71234890', '+51912345678', 'Certificación OSHA General Industry', 'Técnico Mecánico Senior', NOW(), NOW()),
(3, NULL, 'María Elena', 'Rojas Quispe', 'maria.rojas@system.local', '40123987', '+51955443322', 'NFPA 70E Seguridad Eléctrica', 'Técnico Electricista', NOW(), NOW()),
(4, NULL, 'Luis Miguel', 'Torres Castillo', 'luis.torres@system.local', '44889922', '+51933221144', 'Operador Certificado Maquinaria Pesada CAT', 'Operador de Maquinaria', NOW(), NOW()),
(5, NULL, 'Ana Sofía', 'Vargas Huamán', 'ana.vargas@system.local', '47990011', '+51977889900', 'Gestión de Mantenimiento Industrial - Lean Maintenance', 'Supervisora de Mantenimiento', NOW(), NOW()),
(6, NULL, 'Jorge Luis', 'Chávez Ramos', 'jorge.chavez@system.local', '42556677', '+51966554433', 'Soldadura Homologada ASME Sec. IX', 'Técnico Soldador', NOW(), NOW()),
(7, NULL, 'Rosa María', 'Medina Flores', 'rosa.medina@system.local', '43112233', '+51944332211', 'Especialista en Neumática e Hidráulica Parker', 'Técnico Hidráulico', NOW(), NOW()),
(8, NULL, 'Pedro Pablo', 'Ramírez Castro', 'pedro.ramirez@system.local', '46778899', '+51988776655', 'Termografía Infrarroja Nivel I (ISO 18436-7)', 'Técnico de Mantenimiento Predictivo', NOW(), NOW()),
(9, NULL, 'Carmen Rosa', 'Salas Morales', 'carmen.salas@system.local', '41998877', '+51922334455', 'Automatización y Control PLC Siemens S7', 'Técnico de Automatización', NOW(), NOW()),
(10, NULL, 'Víctor Manuel', 'Benites Cruz', 'victor.benites@system.local', '48334455', '+51999887766', 'Mantenimiento de Motores Diésel de Alta Potencia', 'Técnico Mecánico de Motores', NOW(), NOW()),
(11, NULL, 'Diana Patricia', 'Espinoza Vega', 'diana.espinoza@system.local', '49556677', '+51911223344', 'Gestión de Repuestos y Logística de Almacén', 'Encargada de Inventarios', NOW(), NOW()),
(12, NULL, 'Gabriel Alejandro', 'Navarro Ríos', 'gabriel.navarro@system.local', '40887766', '+51944556677', 'Metrología y Calibración de Instrumentos', 'Técnico Metrólogo', NOW(), NOW()),
(13, NULL, 'Lucia Beatriz', 'Salazar León', 'lucia.salazar@system.local', '45221144', '+51977665544', 'Seguridad, Salud Ocupacional y Medio Ambiente (SSOMA)', 'Especialista SSOMA', NOW(), NOW()),
(14, NULL, 'Fernando José', 'Acosta Paredes', 'fernando.acosta@system.local', '43665544', '+51933445566', 'Mantenimiento Preventivo de Plantas Industriales', 'Jefe de Taller', NOW(), NOW());

-- migrate:down

DELETE FROM workers;
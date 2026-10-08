-- migrate:up

INSERT INTO brands (id, name, description, created_at, updated_at) VALUES
(1, 'Bosch', 'Empresa multinacional de ingeniería y tecnología, fabricante de autopartes y herramientas industriales.', NOW(), NOW()),
(2, 'Siemens', 'Compañía global líder en automatización industrial, electrificación y digitalización.', NOW(), NOW()),
(3, 'Caterpillar', 'Fabricante líder mundial de maquinaria de construcción, minería y motores diésel.', NOW(), NOW()),
(4, 'Komatsu', 'Fabricante global de equipos para construcción, minería, forestal y servicios industriales.', NOW(), NOW()),
(5, 'Schneider Electric', 'Especialista global en gestión energética y automatización industrial.', NOW(), NOW()),
(6, 'SKF', 'Lider mundial en fabricación de rodamientos, sellos, sistemas de lubricación y servicios de mantenimiento.', NOW(), NOW()),
(7, 'Parker Hannifin', 'Líder mundial en tecnologías de movimiento y control, sistemas hidráulicos y neumáticos.', NOW(), NOW());

-- migrate:down

DELETE FROM brands;
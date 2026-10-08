-- migrate:up

INSERT INTO oil_types (id, name, description) VALUES
(1, 'Aceite hidráulico', 'Lubricante utilizado en sistemas y circuitos hidráulicos industriales.'),
(2, 'Aceite para engranajes', 'Lubricante diseñado para cajas reductoras, transmisiones y sistemas de engranajes.'),
(3, 'Aceite para motores', 'Lubricante utilizado en motores de combustión interna.'),
(4, 'Aceite para turbinas', 'Lubricante utilizado en turbinas de vapor, gas e hidráulicas.'),
(5, 'Aceite para compresores', 'Lubricante utilizado en compresores de aire, gas y otros equipos de compresión.'),
(6, 'Aceite para cadenas', 'Lubricante diseñado para cadenas y sistemas de transmisión por cadena.'),
(7, 'Aceite para guías y correderas', 'Lubricante utilizado en guías, bancadas y correderas de máquinas herramienta.'),
(8, 'Aceite de circulación', 'Lubricante utilizado en sistemas de lubricación por circulación continua.'),
(9, 'Aceite para rodamientos', 'Lubricante utilizado en rodamientos y cojinetes que requieren lubricación con aceite.'),
(10, 'Aceite para transformadores', 'Fluido dieléctrico utilizado para aislamiento y refrigeración de transformadores eléctricos.'),
(11, 'Fluido de transferencia de calor', 'Fluido utilizado para transferir y controlar calor en sistemas industriales.'),
(12, 'Aceite para corte', 'Lubricante o fluido utilizado en procesos de mecanizado y corte de metales.'),
(13, 'Grasa lubricante', 'Lubricante semisólido utilizado en rodamientos, cojinetes, engranajes y otros componentes.'),
(14, 'Fluido hidráulico biodegradable', 'Fluido hidráulico formulado para aplicaciones donde se requiere menor impacto ambiental.');

-- migrate:down

DELETE FROM oil_types;
-- migrate:up

INSERT INTO oils (id, oil_brand_id, oil_type_id, name, description) VALUES
(1, 1, 1, 'Shell Tellus S2 M 46', 'Aceite hidráulico de alto rendimiento para sistemas industriales y equipos móviles.'),
(2, 1, 10, 'Shell Diala S4 ZX-G', 'Fluido aislante inhibido de alta calidad para transformadores eléctricos.'),
(3, 2, 2, 'Mobilgear 600 XP 220', 'Aceite para engranajes industriales de alta carga y protección contra el desgaste.'),
(4, 2, 5, 'Mobil Rarus 427', 'Aceite sintético para compresores de aire reciprocantes y de tornillo.'),
(5, 3, 3, 'Castrol GTX 20W-50', 'Aceite multigrado formulado para proteger motores de combustión interna.'),
(6, 3, 6, 'Castrol Tribol Chain Lube', 'Lubricante sintético diseñado para cadenas expuestas a altas temperaturas.'),
(7, 4, 4, 'Chevron Regal R&O 46', 'Aceite lubricante premium para turbinas de vapor, gas e hidráulicas.'),
(8, 4, 14, 'Chevron Clarity Synthetic Hydraulic Oil AW 46', 'Fluido hidráulico ecológico y biodegradable para aplicaciones con riesgo ambiental.'),
(9, 5, 7, 'Total Carter EP 320', 'Aceite para engranajes bajo condiciones severas de operación.'),
(10, 6, 11, 'Petro-Canada Calflo AF', 'Fluido térmico de transferencia de calor para sistemas cerrados de calefacción.'),
(11, 7, 13, 'SKF LGMT 2', 'Grasa para uso general industrial y automotriz con aceite base mineral y espesante de litio.'),
(12, 8, 12, 'Fuchs Ecocut 715', 'Aceite de corte para procesos de mecanizado general de metales ferrosos.'),
(13, 9, 9, 'Klüberoil 4 N 150', 'Aceite sintético especial para engranajes y rodamientos sometidos a altas cargas.'),
(14, 10, 8, 'Chevron GST Oil 32', 'Aceite de circulación de alta calidad para sistemas de lubricación continua.');

-- migrate:down

DELETE FROM oils;
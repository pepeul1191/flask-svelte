-- migrate:up

INSERT INTO brand_models (id, brand_id, name, description, created_at, updated_at) VALUES
-- Modelos para Bosch (brand_id = 1)
(1, 1, 'GSR 18V-50', 'Taladro destornillador a batería de 18V con motor sin escobillas.', NOW(), NOW()),
(2, 1, 'GBH 2-28', 'Martillo perforador rotativo SDS-plus con control de vibración.', NOW(), NOW()),
(3, 1, 'GWS 18V-10', 'Amoladora angular a batería de 115mm de alto rendimiento.', NOW(), NOW()),
(4, 1, 'GST 18V-LI', 'Sierra de calar profesional a batería con guía de precisión.', NOW(), NOW()),
(5, 1, 'GSB 18V-85 C', 'Taladro percutor inteligente con conectividad Bluetooth.', NOW(), NOW()),
(6, 1, 'GOP 18V-28', 'Multiherramienta oscilante profesional para cortes y lijado.', NOW(), NOW()),

-- Modelos para Siemens (brand_id = 2)
(7, 2, 'SIMATIC S7-1200', 'Controlador lógico programable (PLC) compacto para automatización modular.', NOW(), NOW()),
(8, 2, 'SIMATIC S7-1500', 'Controlador avanzado para plantas de alta exigencia y velocidad.', NOW(), NOW()),
(9, 2, 'SINAMICS G120', 'Variador de frecuencia modular para control de motores industriales.', NOW(), NOW()),
(10, 2, 'SIMATIC TP700 Comfort', 'Panel de operador táctil HMI de 7 pulgadas con visualización avanzada.', NOW(), NOW()),
(11, 2, 'SITRANS P DS III', 'Transmisor de presión diferencial y manométrica de alta precisión.', NOW(), NOW()),
(12, 2, 'LOGO! 8', 'Módulo lógico universal básico para automatización en pequeña escala.', NOW(), NOW()),

-- Modelos para Caterpillar (brand_id = 3)
(13, 3, 'CAT 320', 'Excavadora hidráulica mediana de alto rendimiento y bajo consumo.', NOW(), NOW()),
(14, 3, 'CAT D6', 'Tractor de cadenas versátil para nivelación y movimiento de tierras.', NOW(), NOW()),
(15, 3, 'CAT 950M', 'Cargador de ruedas mediano con tecnología avanzada de pesaje.', NOW(), NOW()),
(16, 3, 'CAT 14M', 'Motoniveladora de alta precisión para proyectos viales y mineros.', NOW(), NOW()),
(17, 3, 'CAT 745', 'Camión articulado de gran capacidad para terrenos difíciles.', NOW(), NOW()),
(18, 3, 'CAT C15', 'Motor diésel industrial de alta potencia para aplicaciones pesadas.', NOW(), NOW()),
(19, 3, 'CAT 289D3', 'Minicargador todoterreno sobre orugas con cabina presurizada.', NOW(), NOW()),

-- Modelos para Komatsu (brand_id = 4)
(20, 4, 'PC200-8M0', 'Excavadora hidráulica estándar de alta durabilidad en construcción.', NOW(), NOW()),
(21, 4, 'D85EX-18', 'Bulldozer oruga de empuje óptimo para minería y obras civiles.', NOW(), NOW()),
(22, 4, 'WA380-8', 'Cargador frontal versátil con excelente eficiencia de combustible.', NOW(), NOW()),
(23, 4, 'GD655-6', 'Motoniveladora de transmisión hidrostática para mantenimiento vial.', NOW(), NOW()),
(24, 4, 'HD785-7', 'Camión de volteo minero rígido de gran tonelaje.', NOW(), NOW()),
(25, 4, 'WA470-8', 'Cargador de ruedas de gran capacidad para canteras y áridos.', NOW(), NOW()),

-- Modelos para Schneider Electric (brand_id = 5)
(26, 5, 'Altivar 312', 'Variador de frecuencia compacto para motores asíncronos trifásicos.', NOW(), NOW()),
(27, 5, 'TeSys D', 'Contactor tripolar de alta seguridad para control de motores y circuitos.', NOW(), NOW()),
(28, 5, 'Acti9 iC60N', 'Interruptor automático termomagnético en riel DIN para protección eléctrica.', NOW(), NOW()),
(29, 5, 'Modicon M221', 'Controlador lógico programable y escalable para máquinas compactas.', NOW(), NOW()),
(30, 5, 'Harmony XB5', 'Pulsadores, selectores y luces piloto plásticas de Ø22 mm.', NOW(), NOW()),
(31, 5, 'EasyPact CVS', 'Interruptor automático en caja moldeada para distribución de energía.', NOW(), NOW()),
(32, 5, 'PowerTag Energy', 'Sensor de energía inalámbrico para submedición en tableros.', NOW(), NOW()),

-- Modelos para SKF (brand_id = 6)
(33, 6, 'Rodamiento Rígido de Bolas 6205', 'Rodamiento de una hilera de bolas de uso industrial estándar.', NOW(), NOW()),
(34, 6, 'Rodamiento de Rodillos Cónicos 32210', 'Diseñado para soportar cargas radiales y axiales combinadas.', NOW(), NOW()),
(35, 6, 'SKF QuickCollect', 'Sensor multifunción portátil para vibración y temperatura.', NOW(), NOW()),
(36, 6, 'SKF TKTL 40', 'Termómetro infrarrojo y de contacto de doble láser.', NOW(), NOW()),
(37, 6, 'SKF TMMI 15', 'Herramienta de alineación de ejes por láser fácil de operar.', NOW(), NOW()),
(38, 6, 'Rodamiento Axiales de Bolas 51112', 'Soporta cargas axiales unidireccionales de alta precisión.', NOW(), NOW()),

-- Modelos para Parker Hannifin (brand_id = 7)
(39, 7, 'Bomba de pistones PVplus', 'Bomba hidráulica de caudal variable para sistemas industriales y móviles.', NOW(), NOW()),
(40, 7, 'Cilindro Hidráulico Series Hmi', 'Cilindro de alta presión y rendimiento para maquinaria pesada.', NOW(), NOW()),
(41, 7, 'Válvula Proporcional D1FP', 'Válvula directriz con control electrónico integrado.', NOW(), NOW()),
(42, 7, 'Manguera Hidráulica 471TC', 'Manguera de alta presión con refuerzo de cuatro espirales de acero.', NOW(), NOW()),
(43, 7, 'Filtro de Retorno Parker 15P', 'Filtro hidráulico de alta retención de partículas para tanques.', NOW(), NOW()),
(44, 7, 'Conector EO-2', 'Racores de compresión sin abocardado para tubos hidráulicos.', NOW(), NOW());

-- migrate:down

DELETE FROM brand_models;
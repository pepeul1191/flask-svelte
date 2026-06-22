-- migrate:up

-- Inicial (levels 1-3) - 4 ejemplos por nivel
INSERT INTO courses (id, name, code, description, sylabus_url, level_id, worker_id) VALUES
-- Inicial 3 años (level_id = 1)
(1, 'Psicomotricidad', 'INI-PSM-01', 'Desarrollo de habilidades motoras gruesas y finas a través del juego', 'sylabus/inicial/demo.pdf', 1, 5),
(2, 'Comunicación Integral', 'INI-COM-01', 'Desarrollo del lenguaje oral y expresión corporal', 'sylabus/inicial/demo.pdf', 1, 8),
(3, 'Matemática Lúdica', 'INI-MAT-01', 'Nociones básicas de cantidad y formas mediante juegos', 'sylabus/inicial/demo.pdf', 1, 12),
(4, 'Arte y Creatividad', 'INI-ART-01', 'Expresión artística con diferentes técnicas y materiales', 'sylabus/inicial/demo.pdf', 1, 15),

-- Inicial 4 años (level_id = 2)
(5, 'Psicomotricidad II', 'INI-PSM-02', 'Coordinación y equilibrio en actividades lúdicas', 'sylabus/inicial/demo.pdf', 2, 7),
(6, 'Comunicación II', 'INI-COM-02', 'Iniciación a la lectura de imágenes y expresión oral', 'sylabus/inicial/demo.pdf', 2, 10),
(7, 'Matemática II', 'INI-MAT-02', 'Números del 1 al 10 y nociones espaciales', 'sylabus/inicial/demo.pdf', 2, 14),
(8, 'Ciencia y Ambiente', 'INI-CIA-01', 'Descubrimiento del entorno natural', 'sylabus/inicial/demo.pdf', 2, 18),

-- Inicial 5 años (level_id = 3)
(9, 'Pre-escritura', 'INI-PRE-01', 'Desarrollo de habilidades para la escritura', 'sylabus/inicial/demo.pdf', 3, 9),
(10, 'Lectoescritura', 'INI-LEC-01', 'Iniciación a la lectura y escritura', 'sylabus/inicial/demo.pdf', 3, 11),
(11, 'Matemática III', 'INI-MAT-03', 'Operaciones básicas y resolución de problemas', 'sylabus/inicial/demo.pdf', 3, 16),
(12, 'Personal Social', 'INI-PES-01', 'Autonomía y habilidades sociales', 'sylabus/inicial/demo.pdf', 3, 20);

-- Primaria (levels 4-9) - 7 ejemplos por nivel
-- 1° Primaria (level_id = 4)
INSERT INTO courses (id, name, code, description, sylabus_url, level_id, worker_id) VALUES
(13, 'Comunicación 1°', 'PRI-COM-101', 'Comprensión lectora y producción de textos', 'sylabus/primaria/demo.pdf', 4, 2),
(14, 'Matemática 1°', 'PRI-MAT-101', 'Números hasta 100, suma y resta', 'sylabus/primaria/demo.pdf', 4, 4),
(15, 'Ciencia y Tecnología 1°', 'PRI-CYT-101', 'Seres vivos y fenómenos naturales', 'sylabus/primaria/demo.pdf', 4, 6),
(16, 'Personal Social 1°', 'PRI-PES-101', 'Historia familiar y espacios de convivencia', 'sylabus/primaria/demo.pdf', 4, 13),
(17, 'Arte y Cultura 1°', 'PRI-ART-101', 'Expresión artística y apreciación cultural', 'sylabus/primaria/demo.pdf', 4, 17),
(18, 'Educación Física 1°', 'PRI-EDF-101', 'Desarrollo psicomotor y hábitos saludables', 'sylabus/primaria/demo.pdf', 4, 19),
(19, 'Inglés 1°', 'PRI-ING-101', 'Vocabulario básico y expresiones cotidianas', 'sylabus/primaria/demo.pdf', 4, 21),

-- 2° Primaria (level_id = 5)
(20, 'Comunicación 2°', 'PRI-COM-201', 'Lectura comprensiva y redacción de oraciones', 'sylabus/primaria/demo.pdf', 5, 3),
(21, 'Matemática 2°', 'PRI-MAT-201', 'Números hasta 1000, multiplicación', 'sylabus/primaria/demo.pdf', 5, 1),
(22, 'Ciencia y Tecnología 2°', 'PRI-CYT-201', 'El cuerpo humano y ecosistemas', 'sylabus/primaria/demo.pdf', 5, 22),
(23, 'Personal Social 2°', 'PRI-PES-201', 'Instituciones y oficios de la comunidad', 'sylabus/primaria/demo.pdf', 5, 23),
(24, 'Arte y Cultura 2°', 'PRI-ART-201', 'Técnicas artísticas y folklore', 'sylabus/primaria/demo.pdf', 5, 24),
(25, 'Educación Física 2°', 'PRI-EDF-201', 'Juegos deportivos y coordinación', 'sylabus/primaria/demo.pdf', 5, 25),
(26, 'Inglés 2°', 'PRI-ING-201', 'Expresiones y vocabulario por temas', 'sylabus/primaria/demo.pdf', 5, 26),

-- 3° Primaria (level_id = 6)
(27, 'Comunicación 3°', 'PRI-COM-301', 'Comprensión de textos narrativos', 'sylabus/primaria/demo.pdf', 6, 27),
(28, 'Matemática 3°', 'PRI-MAT-301', 'División, fracciones y geometría', 'sylabus/primaria/demo.pdf', 6, 28),
(29, 'Ciencia y Tecnología 3°', 'PRI-CYT-301', 'Materia y energía', 'sylabus/primaria/demo.pdf', 6, 29),
(30, 'Personal Social 3°', 'PRI-PES-301', 'Historia del Perú antiguo', 'sylabus/primaria/demo.pdf', 6, 30),
(31, 'Arte y Cultura 3°', 'PRI-ART-301', 'Teatro y expresión corporal', 'sylabus/primaria/demo.pdf', 6, 5),
(32, 'Educación Física 3°', 'PRI-EDF-301', 'Deportes y trabajo en equipo', 'sylabus/primaria/demo.pdf', 6, 8),
(33, 'Inglés 3°', 'PRI-ING-301', 'Descripciones y conversaciones simples', 'sylabus/primaria/demo.pdf', 6, 10),

-- 4° Primaria (level_id = 7)
(34, 'Comunicación 4°', 'PRI-COM-401', 'Textos descriptivos y argumentativos', 'sylabus/primaria/demo.pdf', 7, 12),
(35, 'Matemática 4°', 'PRI-MAT-401', 'Decimales y medidas', 'sylabus/primaria/demo.pdf', 7, 14),
(36, 'Ciencia y Tecnología 4°', 'PRI-CYT-401', 'Sistema solar y biodiversidad', 'sylabus/primaria/demo.pdf', 7, 16),
(37, 'Personal Social 4°', 'PRI-PES-401', 'Historia del Perú medieval', 'sylabus/primaria/demo.pdf', 7, 18),
(38, 'Arte y Cultura 4°', 'PRI-ART-401', 'Música y danzas peruanas', 'sylabus/primaria/demo.pdf', 7, 20),
(39, 'Educación Física 4°', 'PRI-EDF-401', 'Atletismo y resistencia', 'sylabus/primaria/demo.pdf', 7, 22),
(40, 'Inglés 4°', 'PRI-ING-401', 'Tiempos verbales básicos', 'sylabus/primaria/demo.pdf', 7, 24),

-- 5° Primaria (level_id = 8)
(41, 'Comunicación 5°', 'PRI-COM-501', 'Comprensión crítica de textos', 'sylabus/primaria/demo.pdf', 8, 26),
(42, 'Matemática 5°', 'PRI-MAT-501', 'Fracciones equivalentes y porcentajes', 'sylabus/primaria/demo.pdf', 8, 28),
(43, 'Ciencia y Tecnología 5°', 'PRI-CYT-501', 'Sistema digestivo y reproductor', 'sylabus/primaria/demo.pdf', 8, 30),
(44, 'Personal Social 5°', 'PRI-PES-501', 'Historia del descubrimiento y colonia', 'sylabus/primaria/demo.pdf', 8, 2),
(45, 'Arte y Cultura 5°', 'PRI-ART-501', 'Arte contemporáneo', 'sylabus/primaria/demo.pdf', 8, 4),
(46, 'Educación Física 5°', 'PRI-EDF-501', 'Voleibol y básquetbol', 'sylabus/primaria/demo.pdf', 8, 6),
(47, 'Inglés 5°', 'PRI-ING-501', 'Presente y pasado simple', 'sylabus/primaria/demo.pdf', 8, 8),

-- 6° Primaria (level_id = 9)
(48, 'Comunicación 6°', 'PRI-COM-601', 'Textos expositivos y académicos', 'sylabus/primaria/demo.pdf', 9, 10),
(49, 'Matemática 6°', 'PRI-MAT-601', 'Razones y proporciones', 'sylabus/primaria/demo.pdf', 9, 12),
(50, 'Ciencia y Tecnología 6°', 'PRI-CYT-601', 'Fenómenos físicos y químicos', 'sylabus/primaria/demo.pdf', 9, 14),
(51, 'Personal Social 6°', 'PRI-PES-601', 'Historia de la independencia y república', 'sylabus/primaria/demo.pdf', 9, 16),
(52, 'Arte y Cultura 6°', 'PRI-ART-601', 'Producción audiovisual', 'sylabus/primaria/demo.pdf', 9, 18),
(53, 'Educación Física 6°', 'PRI-EDF-601', 'Fútbol y natación', 'sylabus/primaria/demo.pdf', 9, 20),
(54, 'Inglés 6°', 'PRI-ING-601', 'Producción de textos en inglés', 'sylabus/primaria/demo.pdf', 9, 22);

-- Secundaria (levels 10-14) - 11 ejemplos por nivel
-- 1° Secundaria (level_id = 10)
INSERT INTO courses (id, name, code, description, sylabus_url, level_id, worker_id) VALUES
(55, 'Comunicación 1° Sec', 'SEC-COM-101', 'Análisis literario y producción textual', 'sylabus/secundaria/demo.pdf', 10, 24),
(56, 'Matemática 1° Sec', 'SEC-MAT-101', 'Números racionales y ecuaciones', 'sylabus/secundaria/demo.pdf', 10, 26),
(57, 'Ciencia y Tecnología 1° Sec', 'SEC-CYT-101', 'Biología celular y química básica', 'sylabus/secundaria/demo.pdf', 10, 28),
(58, 'Historia 1° Sec', 'SEC-HIS-101', 'Historia universal antigua', 'sylabus/secundaria/demo.pdf', 10, 30),
(59, 'Geografía 1° Sec', 'SEC-GEO-101', 'Geografía física', 'sylabus/secundaria/demo.pdf', 10, 1),
(60, 'Formación Ciudadana 1° Sec', 'SEC-FCC-101', 'Derechos y deberes', 'sylabus/secundaria/demo.pdf', 10, 3),
(61, 'Inglés 1° Sec', 'SEC-ING-101', 'Presente perfecto y futuro', 'sylabus/secundaria/demo.pdf', 10, 5),
(62, 'Arte 1° Sec', 'SEC-ART-101', 'Historia del arte', 'sylabus/secundaria/demo.pdf', 10, 7),
(63, 'Educación Física 1° Sec', 'SEC-EDF-101', 'Acondicionamiento físico', 'sylabus/secundaria/demo.pdf', 10, 9),
(64, 'Religión 1° Sec', 'SEC-REL-101', 'Formación espiritual', 'sylabus/secundaria/demo.pdf', 10, 11),
(65, 'Tutoría 1° Sec', 'SEC-TUT-101', 'Orientación personal', 'sylabus/secundaria/demo.pdf', 10, 13),

-- 2° Secundaria (level_id = 11)
(66, 'Comunicación 2° Sec', 'SEC-COM-201', 'Literatura universal', 'sylabus/secundaria/demo.pdf', 11, 15),
(67, 'Matemática 2° Sec', 'SEC-MAT-201', 'Álgebra y funciones', 'sylabus/secundaria/demo.pdf', 11, 17),
(68, 'Ciencia y Tecnología 2° Sec', 'SEC-CYT-201', 'Física mecánica', 'sylabus/secundaria/demo.pdf', 11, 19),
(69, 'Historia 2° Sec', 'SEC-HIS-201', 'Historia medieval', 'sylabus/secundaria/demo.pdf', 11, 21),
(70, 'Geografía 2° Sec', 'SEC-GEO-201', 'Geografía humana', 'sylabus/secundaria/demo.pdf', 11, 23),
(71, 'Formación Ciudadana 2° Sec', 'SEC-FCC-201', 'Participación ciudadana', 'sylabus/secundaria/demo.pdf', 11, 25),
(72, 'Inglés 2° Sec', 'SEC-ING-201', 'Condicionales', 'sylabus/secundaria/demo.pdf', 11, 27),
(73, 'Arte 2° Sec', 'SEC-ART-201', 'Arte peruano', 'sylabus/secundaria/demo.pdf', 11, 29),
(74, 'Educación Física 2° Sec', 'SEC-EDF-201', 'Gimnasia deportiva', 'sylabus/secundaria/demo.pdf', 11, 2),
(75, 'Religión 2° Sec', 'SEC-REL-201', 'Valores éticos', 'sylabus/secundaria/demo.pdf', 11, 4),
(76, 'Tutoría 2° Sec', 'SEC-TUT-201', 'Proyecto de vida', 'sylabus/secundaria/demo.pdf', 11, 6),

-- 3° Secundaria (level_id = 12)
(77, 'Comunicación 3° Sec', 'SEC-COM-301', 'Literatura latinoamericana', 'sylabus/secundaria/demo.pdf', 12, 8),
(78, 'Matemática 3° Sec', 'SEC-MAT-301', 'Geometría analítica', 'sylabus/secundaria/demo.pdf', 12, 10),
(79, 'Ciencia y Tecnología 3° Sec', 'SEC-CYT-301', 'Química orgánica', 'sylabus/secundaria/demo.pdf', 12, 12),
(80, 'Historia 3° Sec', 'SEC-HIS-301', 'Historia moderna', 'sylabus/secundaria/demo.pdf', 12, 14),
(81, 'Geografía 3° Sec', 'SEC-GEO-301', 'Geografía económica', 'sylabus/secundaria/demo.pdf', 12, 16),
(82, 'Formación Ciudadana 3° Sec', 'SEC-FCC-301', 'Derechos humanos', 'sylabus/secundaria/demo.pdf', 12, 18),
(83, 'Inglés 3° Sec', 'SEC-ING-301', 'Voz pasiva', 'sylabus/secundaria/demo.pdf', 12, 20),
(84, 'Arte 3° Sec', 'SEC-ART-301', 'Arte contemporáneo', 'sylabus/secundaria/demo.pdf', 12, 22),
(85, 'Educación Física 3° Sec', 'SEC-EDF-301', 'Básquetbol competitivo', 'sylabus/secundaria/demo.pdf', 12, 24),
(86, 'Religión 3° Sec', 'SEC-REL-301', 'Filosofía religiosa', 'sylabus/secundaria/demo.pdf', 12, 26),
(87, 'Tutoría 3° Sec', 'SEC-TUT-301', 'Liderazgo', 'sylabus/secundaria/demo.pdf', 12, 28),

-- 4° Secundaria (level_id = 13)
(88, 'Comunicación 4° Sec', 'SEC-COM-401', 'Literatura peruana', 'sylabus/secundaria/demo.pdf', 13, 30),
(89, 'Matemática 4° Sec', 'SEC-MAT-401', 'Trigonometría', 'sylabus/secundaria/demo.pdf', 13, 1),
(90, 'Ciencia y Tecnología 4° Sec', 'SEC-CYT-401', 'Biología molecular', 'sylabus/secundaria/demo.pdf', 13, 3),
(91, 'Historia 4° Sec', 'SEC-HIS-401', 'Historia contemporánea', 'sylabus/secundaria/demo.pdf', 13, 5),
(92, 'Geografía 4° Sec', 'SEC-GEO-401', 'Geopolítica', 'sylabus/secundaria/demo.pdf', 13, 7),
(93, 'Formación Ciudadana 4° Sec', 'SEC-FCC-401', 'Constitución política', 'sylabus/secundaria/demo.pdf', 13, 9),
(94, 'Inglés 4° Sec', 'SEC-ING-401', 'Reported speech', 'sylabus/secundaria/demo.pdf', 13, 11),
(95, 'Arte 4° Sec', 'SEC-ART-401', 'Gestión cultural', 'sylabus/secundaria/demo.pdf', 13, 13),
(96, 'Educación Física 4° Sec', 'SEC-EDF-401', 'Voleibol competitivo', 'sylabus/secundaria/demo.pdf', 13, 15),
(97, 'Religión 4° Sec', 'SEC-REL-401', 'Ética social', 'sylabus/secundaria/demo.pdf', 13, 17),
(98, 'Tutoría 4° Sec', 'SEC-TUT-401', 'Orientación vocacional', 'sylabus/secundaria/demo.pdf', 13, 19),

-- 5° Secundaria (level_id = 14)
(99, 'Comunicación 5° Sec', 'SEC-COM-501', 'Comunicación audiovisual', 'sylabus/secundaria/demo.pdf', 14, 21),
(100, 'Matemática 5° Sec', 'SEC-MAT-501', 'Estadística y probabilidad', 'sylabus/secundaria/demo.pdf', 14, 23),
(101, 'Ciencia y Tecnología 5° Sec', 'SEC-CYT-501', 'Física cuántica', 'sylabus/secundaria/demo.pdf', 14, 25),
(102, 'Historia 5° Sec', 'SEC-HIS-501', 'Historia del Perú siglo XX', 'sylabus/secundaria/demo.pdf', 14, 27),
(103, 'Geografía 5° Sec', 'SEC-GEO-501', 'Problemas ambientales', 'sylabus/secundaria/demo.pdf', 14, 29),
(104, 'Formación Ciudadana 5° Sec', 'SEC-FCC-501', 'Proyectos de desarrollo', 'sylabus/secundaria/demo.pdf', 14, 2),
(105, 'Inglés 5° Sec', 'SEC-ING-501', 'Academic writing', 'sylabus/secundaria/demo.pdf', 14, 4),
(106, 'Arte 5° Sec', 'SEC-ART-501', 'Portafolio artístico', 'sylabus/secundaria/demo.pdf', 14, 6),
(107, 'Educación Física 5° Sec', 'SEC-EDF-501', 'Preparación deportiva', 'sylabus/secundaria/demo.pdf', 14, 8),
(108, 'Religión 5° Sec', 'SEC-REL-501', 'Proyecto de vida cristiano', 'sylabus/secundaria/demo.pdf', 14, 10),
(109, 'Tutoría 5° Sec', 'SEC-TUT-501', 'Preparación para la vida universitaria', 'sylabus/secundaria/demo.pdf', 14, 12);

-- Talleres (levels 15-17) - 3 ejemplos por nivel
-- Talleres de Arte (level_id = 15)
INSERT INTO courses (id, name, code, description, sylabus_url, level_id, worker_id) VALUES
(110, 'Taller de Pintura', 'TLL-ART-001', 'Técnicas de acuarela, óleo y acrílico', 'sylabus/talleres/demo.pdf', 15, 14),
(111, 'Taller de Teatro', 'TLL-ART-002', 'Expresión corporal e improvisación teatral', 'sylabus/talleres/demo.pdf', 15, 16),
(112, 'Taller de Música', 'TLL-ART-003', 'Iniciación musical y práctica instrumental', 'sylabus/talleres/demo.pdf', 15, 18),

-- Talleres de Deporte (level_id = 16)
(113, 'Taller de Fútbol', 'TLL-DEP-001', 'Fundamentos técnicos y tácticos del fútbol', 'sylabus/talleres/demo.pdf', 16, 20),
(114, 'Taller de Básquetbol', 'TLL-DEP-002', 'Técnica y estrategia en básquetbol', 'sylabus/talleres/demo.pdf', 16, 22),
(115, 'Taller de Natación', 'TLL-DEP-003', 'Estilos de natación y salvamento acuático', 'sylabus/talleres/demo.pdf', 16, 24),

-- Círculos de Estudio (level_id = 17)
(116, 'Círculo de Matemática', 'TLL-CIR-001', 'Preparación para concursos matemáticos', 'sylabus/circulos/demo.pdf', 17, 26),
(117, 'Círculo de Ciencias', 'TLL-CIR-002', 'Proyectos de investigación científica', 'sylabus/circulos/demo.pdf', 17, 28),
(118, 'Círculo de Robótica', 'TLL-CIR-003', 'Programación y construcción de robots', 'sylabus/circulos/demo.pdf', 17, 30);

-- migrate:down

DELETE FROM courses WHERE id BETWEEN 1 AND 118;
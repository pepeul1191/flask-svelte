-- migrate:up

INSERT INTO machines (id, client_id, model_id, name, code, serial_number) VALUES
(1, 1, 5, 'Compresor de Tornillo Principal', 'COMP-001-IND', 'SN-CMP-987123'),
(2, 1, 12, 'Torno CNC de Alta Presición', 'CNC-002-IND', 'SN-CNC-456789'),
(3, 1, 18, 'Puente Grúa 5 Toneladas', 'CRANE-003-IND', 'SN-CRN-112233'),
(4, 1, 24, 'Bomba Centrífuga de Agua', 'PUMP-004-IND', 'SN-PMP-778899'),
(5, 1, 30, 'Generador Diesel de Emergencia', 'GEN-005-IND', 'SN-GEN-554433'),
(6, 2, 8, 'Excavadora Hidráulica Mediana', 'EXC-101-MIN', 'SN-EXC-332211'),
(7, 2, 15, 'Cargador Frontal de Ruedas', 'WLD-102-MIN', 'SN-WLD-667788'),
(8, 2, 41, 'Camión Minero Articulado', 'TRK-103-MIN', 'SN-TRK-990011');

-- migrate:down

DELETE FROM machines;
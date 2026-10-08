-- migrate:up

INSERT INTO oil_brands (id, name, description) VALUES
(1, 'Shell', 'Fabricante de lubricantes y aceites industriales para maquinaria.'),
(2, 'Mobil', 'Marca de lubricantes industriales y aceites para maquinaria y equipos.'),
(3, 'Castrol', 'Fabricante de lubricantes para aplicaciones industriales y automotrices.'),
(4, 'Chevron', 'Fabricante de lubricantes y productos para mantenimiento industrial.'),
(5, 'TotalEnergies', 'Marca de lubricantes para aplicaciones industriales y maquinaria.'),
(6, 'Petro-Canada', 'Fabricante de lubricantes y aceites de alto rendimiento.'),
(7, 'SKF', 'Fabricante de lubricantes y soluciones para mantenimiento de rodamientos y maquinaria.'),
(8, 'Fuchs', 'Fabricante especializado en lubricantes industriales y productos de lubricación.'),
(9, 'Klüber Lubrication', 'Especialista en lubricantes especiales para aplicaciones industriales.'),
(10, 'Chevron Phillips', 'Proveedor de productos y soluciones relacionados con lubricación industrial.');

-- migrate:down

DELETE FROM oil_brands;
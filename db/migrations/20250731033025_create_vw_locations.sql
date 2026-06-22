-- migrate:up

CREATE VIEW vw_locations AS
SELECT 
  D.id AS district_id,
  CONCAT_WS(', ', D.name, P.name, DE.name) AS full_name
FROM districts D
INNER JOIN provinces P ON D.province_id = P.id
INNER JOIN departments DE ON P.department_id = DE.id;

-- migrate:down

DROP VIEW vw_locations;
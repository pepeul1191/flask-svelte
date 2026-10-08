-- migrate:up

DROP VIEW vw_locations;

CREATE VIEW vw_locations AS
SELECT 
  D.id AS id,
  CONCAT_WS(', ', D.name, P.name, DE.name) AS name
FROM districts D
INNER JOIN provinces P ON D.province_id = P.id
INNER JOIN departments DE ON P.department_id = DE.id;

-- migrate:down

DROP VIEW IF EXISTS vw_locations;

CREATE VIEW vw_locations AS
SELECT 
  D.id AS district_id,
  CONCAT_WS(', ', D.name, P.name, DE.name) AS full_name
FROM districts D
INNER JOIN provinces P ON D.province_id = P.id
INNER JOIN departments DE ON P.department_id = DE.id;
-- migrate:up

CREATE VIEW vw_workers AS
SELECT
    w.id AS worker_id,
    w.code,
    w.bio,
    w.person_id,

    p.names,
    p.last_names,
    p.document_number,
    p.sex_id,
    p.document_type_id,
    p.image_url,
    p.birth_date,
    p.created,
    p.updated

FROM workers w
INNER JOIN persons p
    ON w.person_id = p.id;

-- migrate:down

DROP VIEW vw_workers;
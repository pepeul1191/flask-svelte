-- migrate:up

CREATE VIEW vw_representatives AS
SELECT
    R.id AS representative_id,
    R.person_id,
    R.email,
    R.user_id,

    P.names,
    P.last_names,
    P.document_number,
    P.sex_id,
    P.document_type_id,
    P.image_url,
    P.birth_date,
    P.created,
    P.updated

FROM representatives R
INNER JOIN persons P
    ON R.person_id = P.id;

-- migrate:down

DROP VIEW vw_representatives;
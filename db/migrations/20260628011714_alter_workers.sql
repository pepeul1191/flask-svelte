-- migrate:up

ALTER TABLE workers
MODIFY code INT NULL;

-- migrate:down

ALTER TABLE workers
MODIFY code INT NOT NULL;

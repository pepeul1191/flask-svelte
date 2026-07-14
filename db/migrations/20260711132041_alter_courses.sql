-- migrate:up

ALTER TABLE courses
MODIFY worker_id INT UNSIGNED NULL;

-- migrate:down

ALTER TABLE courses
MODIFY worker_id INT UNSIGNED NOT NULL;
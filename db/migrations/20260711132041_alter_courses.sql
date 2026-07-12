-- migrate:up

ALTER TABLE courses
MODIFY COLUMN worker_id INT UNSIGNED NULL;

ALTER TABLE courses
DROP FOREIGN KEY fk_courses_worker;

ALTER TABLE courses
ADD CONSTRAINT fk_courses_worker
  FOREIGN KEY (worker_id)
  REFERENCES workers(id)
  ON UPDATE CASCADE
  ON DELETE SET NULL;


-- migrate:down

ALTER TABLE courses
DROP FOREIGN KEY fk_courses_worker;

ALTER TABLE courses
MODIFY COLUMN worker_id INT UNSIGNED NOT NULL;

ALTER TABLE courses
ADD CONSTRAINT fk_courses_worker
  FOREIGN KEY (worker_id)
  REFERENCES workers(id)
  ON UPDATE CASCADE
  ON DELETE RESTRICT;
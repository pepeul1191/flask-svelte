-- migrate:up

ALTER TABLE courses
ADD COLUMN branch_id INT UNSIGNED NULL AFTER level_id;

ALTER TABLE courses
ADD CONSTRAINT fk_courses_branch
    FOREIGN KEY (branch_id)
    REFERENCES branches(id)
    ON DELETE SET NULL;

CREATE INDEX idx_courses_branch_id ON courses(branch_id);

-- migrate:down

ALTER TABLE courses
DROP INDEX idx_courses_branch_id;

ALTER TABLE courses
DROP FOREIGN KEY fk_courses_branch;

ALTER TABLE courses
DROP COLUMN branch_id;
-- migrate:up

ALTER TABLE courses
ADD COLUMN course_branch_id INT UNSIGNED NULL AFTER level_id;

ALTER TABLE courses
ADD CONSTRAINT fk_courses_branch
    FOREIGN KEY (course_branch_id)
    REFERENCES course_branches(id)
    ON DELETE SET NULL;

CREATE INDEX idx_courses_course_branch_id ON courses(course_branch_id);

-- migrate:down

ALTER TABLE courses
DROP FOREIGN KEY fk_courses_branch;

ALTER TABLE courses
DROP INDEX idx_courses_course_branch_id;

ALTER TABLE courses
DROP COLUMN course_branch_id;
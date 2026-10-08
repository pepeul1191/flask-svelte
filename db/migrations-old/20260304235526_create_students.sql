-- migrate:up

CREATE TABLE students (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  code INT,
  email VARCHAR(100),
  person_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED,
  PRIMARY KEY (id),
  CONSTRAINT fk_students_person FOREIGN KEY (person_id) REFERENCES persons(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `students` 
ADD CONSTRAINT `students_email_unique` UNIQUE (`email`),
ADD CONSTRAINT `students_user_id_unique` UNIQUE (`user_id`);

-- migrate:down

ALTER TABLE `students`
DROP INDEX `students_email_unique`,
DROP INDEX `students_user_id_unique`;
DROP TABLE students;

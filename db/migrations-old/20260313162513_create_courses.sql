-- migrate:up

CREATE TABLE courses (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  code VARCHAR(20) NOT NULL,
  description TEXT,
  sylabus_url VARCHAR(100),
  level_id INT UNSIGNED NOT NULL,
  worker_id INT UNSIGNED NOT NULL,

  PRIMARY KEY (id),

  CONSTRAINT fk_courses_level
    FOREIGN KEY (level_id)
    REFERENCES levels(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

  CONSTRAINT fk_courses_worker
    FOREIGN KEY (worker_id)
    REFERENCES workers(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- migrate:down

DROP TABLE IF EXISTS courses;
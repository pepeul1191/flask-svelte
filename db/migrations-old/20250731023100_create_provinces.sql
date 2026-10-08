-- migrate:up

CREATE TABLE provinces (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  department_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_provinces_department_id (department_id),
  CONSTRAINT fk_provinces_department
    FOREIGN KEY (department_id)
    REFERENCES departments(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- migrate:down

DROP TABLE provinces;
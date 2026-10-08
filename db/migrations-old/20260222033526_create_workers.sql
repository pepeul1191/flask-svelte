-- migrate:up

CREATE TABLE workers (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  code INT NOT NULL,
  bio TEXT,
  person_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_workers_person FOREIGN KEY (person_id) REFERENCES persons(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- migrate:down

DROP TABLE workers;
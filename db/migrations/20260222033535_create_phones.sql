-- migrate:up

CREATE TABLE phones (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  person_id INT UNSIGNED NOT NULL,
  description VARCHAR(40) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_phones_person FOREIGN KEY (person_id) REFERENCES persons(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- migrate:down

DROP TABLE phones;
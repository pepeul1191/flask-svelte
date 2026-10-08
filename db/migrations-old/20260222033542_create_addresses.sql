-- migrate:up

CREATE TABLE addresses (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  person_id INT UNSIGNED NOT NULL,
  description VARCHAR(40) NOT NULL,
  address VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_addresses_person FOREIGN KEY (person_id) REFERENCES persons(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- migrate:down

DROP TABLE addresses;
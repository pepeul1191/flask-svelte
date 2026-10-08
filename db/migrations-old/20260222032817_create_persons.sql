-- migrate:up

CREATE TABLE persons (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  names VARCHAR(45) NOT NULL,
  last_names VARCHAR(45) NOT NULL,
  document_number VARCHAR(12) NOT NULL,
  sex_id INT UNSIGNED NOT NULL,
  document_type_id INT UNSIGNED NOT NULL,
  image_url VARCHAR(70) NOT NULL DEFAULT 'img/user.png',
  birth_date DATE NOT NULL,
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT fk_persons_sex FOREIGN KEY (sex_id) REFERENCES sexs(id),
  CONSTRAINT fk_persons_document_type FOREIGN KEY (document_type_id) REFERENCES document_types(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- migrate:down

DROP TABLE persons;
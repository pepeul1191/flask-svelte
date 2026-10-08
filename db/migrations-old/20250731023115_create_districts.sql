-- migrate:up

CREATE TABLE districts (
  id INT UNSIGNED AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  province_id INT UNSIGNED NOT NULL,

  PRIMARY KEY (id),

  INDEX idx_districts_province_id (province_id),

  CONSTRAINT fk_districts_province
    FOREIGN KEY (province_id)
    REFERENCES provinces(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- migrate:down

DROP TABLE districts;
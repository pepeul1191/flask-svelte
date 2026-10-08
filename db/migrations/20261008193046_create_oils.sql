-- migrate:up

CREATE TABLE oils (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  oil_brand_id INT UNSIGNED NOT NULL,
  oil_type_id INT UNSIGNED NOT NULL,
  name VARCHAR(150) NOT NULL,
  description TEXT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_oils_oil_brand_id (oil_brand_id),
  KEY idx_oils_oil_type_id (oil_type_id),
  CONSTRAINT fk_oils_oil_brand FOREIGN KEY (oil_brand_id) REFERENCES oil_brands (id) ON DELETE CASCADE,
  CONSTRAINT fk_oils_oil_type FOREIGN KEY (oil_type_id) REFERENCES oil_types (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- migrate:down

DROP TABLE oils;
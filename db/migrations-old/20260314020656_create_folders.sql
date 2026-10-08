-- migrate:up
CREATE TABLE folders (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  parent_id INT UNSIGNED NULL,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_folders_parent_id (parent_id),
  CONSTRAINT fk_folders_parent
    FOREIGN KEY (parent_id) REFERENCES folders(id)
    ON DELETE CASCADE
);

-- migrate:down
DROP TABLE IF EXISTS folders;
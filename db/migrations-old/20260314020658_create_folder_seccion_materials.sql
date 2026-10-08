-- migrate:up
CREATE TABLE folder_seccion_materials (
  id INT UNSIGNED NOT NULL,
  section_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  KEY idx_fsm_section_id (section_id),
  CONSTRAINT fk_fsm_folder
    FOREIGN KEY (id) REFERENCES folders(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_fsm_section
    FOREIGN KEY (section_id) REFERENCES sections(id)
    ON DELETE CASCADE
);

-- migrate:down
DROP TABLE IF EXISTS folder_seccion_materials;
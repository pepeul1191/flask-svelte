-- migrate:up
CREATE TABLE folder_common_materials (
  id INT UNSIGNED NOT NULL,
  course_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (id),
  KEY idx_fcm_course_id (course_id),
  CONSTRAINT fk_fcm_folder
    FOREIGN KEY (id) REFERENCES folders(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_fcm_course
    FOREIGN KEY (course_id) REFERENCES courses(id)
    ON DELETE CASCADE
);

-- migrate:down
DROP TABLE IF EXISTS folder_common_materials;
-- migrate:up
CREATE TABLE sections (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(45) NOT NULL,
    code VARCHAR(20),
    description TEXT,
    image_url VARCHAR(100),
    course_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- migrate:down
DROP TABLE sections;
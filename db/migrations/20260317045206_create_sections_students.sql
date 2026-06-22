-- migrate:up

CREATE TABLE sections_students (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    section_id INT UNSIGNED NOT NULL,
    student_id INT UNSIGNED NOT NULL,

    CONSTRAINT uq_swr_unique_combination
        UNIQUE (section_id, student_id),

    CONSTRAINT fk_swr2_section
        FOREIGN KEY (section_id)
        REFERENCES sections(id),

    CONSTRAINT fk_swr_student
        FOREIGN KEY (student_id)
        REFERENCES students(id)
);

-- migrate:down

DROP TABLE sections_students;

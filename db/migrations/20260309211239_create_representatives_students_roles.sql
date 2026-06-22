-- migrate:up

CREATE TABLE representatives_students_roles (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    representative_id INT UNSIGNED NOT NULL,
    student_id INT UNSIGNED NOT NULL,
    representative_role_id INT UNSIGNED NOT NULL,

    CONSTRAINT uq_rsr_unique_combination
        UNIQUE (representative_id, student_id, representative_role_id),

    CONSTRAINT fk_rsr_representative
        FOREIGN KEY (representative_id)
        REFERENCES representatives(id),

    CONSTRAINT fk_rsr_student
        FOREIGN KEY (student_id)
        REFERENCES students(id),

    CONSTRAINT fk_rsr_role
        FOREIGN KEY (representative_role_id)
        REFERENCES representative_roles(id)
);

-- migrate:down

DROP TABLE representatives_students_roles;
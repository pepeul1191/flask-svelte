-- migrate:up

CREATE TABLE sections_workers_roles (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    section_id INT UNSIGNED NOT NULL,
    worker_id INT UNSIGNED NOT NULL,
    worker_role_id INT UNSIGNED NOT NULL,

    CONSTRAINT uq_swr_unique_combination
        UNIQUE (section_id, worker_id, worker_role_id),

    CONSTRAINT fk_swr_section
        FOREIGN KEY (section_id)
        REFERENCES sections(id),

    CONSTRAINT fk_swr_worker
        FOREIGN KEY (worker_id)
        REFERENCES workers(id),

    CONSTRAINT fk_swr_role
        FOREIGN KEY (worker_role_id)
        REFERENCES worker_roles(id)
);

-- migrate:down

DROP TABLE sections_workers_roles;

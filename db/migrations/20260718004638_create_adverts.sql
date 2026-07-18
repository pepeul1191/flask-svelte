-- migrate:up

CREATE TABLE adverts (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    header VARCHAR(100) NOT NULL,
    description TEXT,
    created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_from DATETIME NULL,
    published_to DATETIME NULL,
    visible BOOLEAN NOT NULL DEFAULT TRUE,
    section_id INT UNSIGNED NOT NULL,
    worker_id INT UNSIGNED NOT NULL,

    PRIMARY KEY (id),

    INDEX idx_adverts_section_id (section_id),
    INDEX idx_adverts_worker_id (worker_id),

    CONSTRAINT fk_adverts_section
        FOREIGN KEY (section_id)
        REFERENCES sections(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_adverts_worker
        FOREIGN KEY (worker_id)
        REFERENCES workers(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- migrate:down

DROP TABLE IF EXISTS adverts;
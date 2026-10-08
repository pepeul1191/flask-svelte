-- migrate:up

ALTER TABLE addresses
  ADD COLUMN district_id INT UNSIGNED AFTER person_id,
  ADD INDEX idx_addresses_district_id (district_id),
  ADD CONSTRAINT fk_addresses_district
    FOREIGN KEY (district_id)
    REFERENCES districts(id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;


-- migrate:down

ALTER TABLE addresses
  DROP FOREIGN KEY fk_addresses_district,
  DROP INDEX idx_addresses_district_id,
  DROP COLUMN district_id;
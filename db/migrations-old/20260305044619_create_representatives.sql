-- migrate:up

CREATE TABLE representatives (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  email VARCHAR(100),
  person_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED,
  PRIMARY KEY (id),
  CONSTRAINT fk_representatives_person FOREIGN KEY (person_id) REFERENCES persons(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE `representatives` 
ADD CONSTRAINT `representatives_email_unique` UNIQUE (`email`),
ADD CONSTRAINT `representatives_user_id_unique` UNIQUE (`user_id`);

-- migrate:down

ALTER TABLE `representatives`
DROP INDEX `representatives_email_unique`,
DROP INDEX `representatives_user_id_unique`;
DROP TABLE representatives;

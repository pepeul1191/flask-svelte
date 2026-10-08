-- migrate:up
ALTER TABLE `workers`
ADD COLUMN `email` VARCHAR(100) NULL AFTER `bio`,
ADD COLUMN `user_id` INT NULL AFTER `email`;

-- migrate:down
ALTER TABLE `workers`
DROP COLUMN `user_id`,
DROP COLUMN `email`;

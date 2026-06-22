-- migrate:up
ALTER TABLE `workers`
ADD CONSTRAINT `workers_email_unique` UNIQUE (`email`),
ADD CONSTRAINT `workers_user_id_unique` UNIQUE (`user_id`);

-- migrate:down
ALTER TABLE `workers`
DROP INDEX `workers_email_unique`,
DROP INDEX `workers_user_id_unique`;
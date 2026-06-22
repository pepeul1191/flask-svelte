-- migrate:up

UPDATE workers SET user_id = NULL WHERE id > 12; 

-- migrate:down

UPDATE workers SET user_id = 13 WHERE id = 13;
UPDATE workers SET user_id = 14 WHERE id = 14;
UPDATE workers SET user_id = 15 WHERE id = 15;
UPDATE workers SET user_id = 16 WHERE id = 16;
UPDATE workers SET user_id = 17 WHERE id = 17;
UPDATE workers SET user_id = 18 WHERE id = 18;
UPDATE workers SET user_id = 19 WHERE id = 19;
UPDATE workers SET user_id = 20 WHERE id = 20;
UPDATE workers SET user_id = 21 WHERE id = 21;
UPDATE workers SET user_id = 22 WHERE id = 22;
UPDATE workers SET user_id = 23 WHERE id = 23;
UPDATE workers SET user_id = 24 WHERE id = 24;
UPDATE workers SET user_id = 25 WHERE id = 25;
UPDATE workers SET user_id = 26 WHERE id = 26;
UPDATE workers SET user_id = 27 WHERE id = 27;
UPDATE workers SET user_id = 28 WHERE id = 28;
UPDATE workers SET user_id = 29 WHERE id = 29;
UPDATE workers SET user_id = 30 WHERE id = 30;
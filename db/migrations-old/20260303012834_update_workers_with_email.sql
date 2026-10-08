-- migrate:up

UPDATE workers SET email = 'usuario1@mail.com', user_id = 1 WHERE id = 1;
UPDATE workers SET email = 'contacto2@mail.com', user_id = 2 WHERE id = 2;
UPDATE workers SET email = 'empleado3@mail.com', user_id = 3 WHERE id = 3;
UPDATE workers SET email = 'trabajador4@mail.com', user_id = 4 WHERE id = 4;
UPDATE workers SET email = 'persona5@mail.com', user_id = 5 WHERE id = 5;
UPDATE workers SET email = 'usuario6@mail.com', user_id = 6 WHERE id = 6;
UPDATE workers SET email = 'contacto7@mail.com', user_id = 7 WHERE id = 7;
UPDATE workers SET email = 'empleado8@mail.com', user_id = 8 WHERE id = 8;
UPDATE workers SET email = 'trabajador9@mail.com', user_id = 9 WHERE id = 9;
UPDATE workers SET email = 'persona10@mail.com', user_id = 10 WHERE id = 10;
UPDATE workers SET email = 'usuario11@mail.com', user_id = 11 WHERE id = 11;
UPDATE workers SET email = 'contacto12@mail.com', user_id = 12 WHERE id = 12;
UPDATE workers SET email = 'empleado13@mail.com', user_id = 13 WHERE id = 13;
UPDATE workers SET email = 'trabajador14@mail.com', user_id = 14 WHERE id = 14;
UPDATE workers SET email = 'persona15@mail.com', user_id = 15 WHERE id = 15;
UPDATE workers SET email = 'usuario16@mail.com', user_id = 16 WHERE id = 16;
UPDATE workers SET email = 'contacto17@mail.com', user_id = 17 WHERE id = 17;
UPDATE workers SET email = 'empleado18@mail.com', user_id = 18 WHERE id = 18;
UPDATE workers SET email = 'trabajador19@mail.com', user_id = 19 WHERE id = 19;
UPDATE workers SET email = 'persona20@mail.com', user_id = 20 WHERE id = 20;
UPDATE workers SET email = 'usuario21@mail.com', user_id = 21 WHERE id = 21;
UPDATE workers SET email = 'contacto22@mail.com', user_id = 22 WHERE id = 22;
UPDATE workers SET email = 'empleado23@mail.com', user_id = 23 WHERE id = 23;
UPDATE workers SET email = 'trabajador24@mail.com', user_id = 24 WHERE id = 24;
UPDATE workers SET email = 'persona25@mail.com', user_id = 25 WHERE id = 25;
UPDATE workers SET email = 'usuario26@mail.com', user_id = 26 WHERE id = 26;
UPDATE workers SET email = 'contacto27@mail.com', user_id = 27 WHERE id = 27;
UPDATE workers SET email = 'empleado28@mail.com', user_id = 28 WHERE id = 28;
UPDATE workers SET email = 'trabajador29@mail.com', user_id = 29 WHERE id = 29;
UPDATE workers SET email = 'persona30@mail.com', user_id = 30 WHERE id = 30;

-- migrate:down

UPDATE workers SET email = null, user_id = null WHERE id <= 30;
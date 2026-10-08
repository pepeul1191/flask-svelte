-- migrate:up

RENAME TABLE employee_roles TO worker_roles;

-- migrate:down

RENAME TABLE worker_roles TO employee_roles;
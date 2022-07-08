CREATE SCHEMA IF NOT EXISTS content;
GRANT ALL PRIVILEGES ON DATABASE content TO docker;


DROP TABLE IF EXISTS roles.user_role;
DROP TABLE IF EXISTS roles.role;


DROP TABLE IF EXISTS users.users;
DROP TABLE IF EXISTS users.refresh;
DROP TABLE IF EXISTS users.social_account;
DROP TABLE IF EXISTS users.auth;

DROP TABLE IF EXISTS alembic_version;
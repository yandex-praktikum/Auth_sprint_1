BEGIN;

CREATE SCHEMA IF NOT EXISTS content;
GRANT ALL PRIVILEGES ON DATABASE content TO docker;

DROP TABLE IF EXISTS users.users CASCADE;
DROP TABLE IF EXISTS users.refresh CASCADE;
DROP TABLE IF EXISTS users.social_account CASCADE;
DROP TABLE IF EXISTS users.auth;

DROP TABLE IF EXISTS alembic_version;

CREATE TABLE users.auth (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    user_agent VARCHAR NOT NULL, 
    auth_type VARCHAR, 
    date_time TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id)
);

CREATE TABLE users.refresh (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    user_agent VARCHAR NOT NULL, 
    refresh_token VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id)
);

CREATE TABLE users.users (
    id UUID NOT NULL, 
    login VARCHAR NOT NULL, 
    name VARCHAR, 
    email VARCHAR NOT NULL, 
    hash_password VARCHAR NOT NULL, 
    role VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (email), 
    UNIQUE (id), 
    UNIQUE (login)
);

CREATE TABLE users.social_account (
    id UUID NOT NULL, 
    user_id UUID NOT NULL, 
    social_type TEXT NOT NULL, 
    social_id TEXT NOT NULL, 
    social_name TEXT NOT NULL, 
    access_token TEXT NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users.users (id), 
    CONSTRAINT social_pk UNIQUE (social_id, social_name)
);

COMMIT;
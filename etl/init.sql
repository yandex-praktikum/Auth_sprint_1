CREATE SCHEMA IF NOT EXISTS content;
GRANT ALL PRIVILEGES ON DATABASE content TO docker;

DROP TABLE IF EXISTS content.person_film_work CASCADE;
DROP TABLE IF EXISTS content.genre_film_work CASCADE;
DROP TABLE IF EXISTS content.film_work;
DROP TABLE IF EXISTS content.person;
DROP TABLE IF EXISTS content.genre;


CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
); 

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone
);

CREATE INDEX IF NOT EXISTS film_work_creation_date_idx ON content.film_work (creation_date);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);
CREATE UNIQUE INDEX IF NOT EXISTS genre_name_idx ON content.genre (name);

CREATE SCHEMA IF NOT EXISTS roles;

DROP TABLE IF EXISTS roles.user_role;
DROP TABLE IF EXISTS roles.role;

CREATE TABLE IF NOT EXISTS roles.role (
    id uuid PRIMARY KEY,
    role TEXT NOT NULL,
    description TEXT,
    rule TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS roles.user_role (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    role_id uuid NOT NULL,
    created timestamp with time zone
);

CREATE SCHEMA IF NOT EXISTS users;

DROP TABLE IF EXISTS users.users;

CREATE TABLE IF NOT EXISTS users.users (
    id uuid PRIMARY KEY,
    login TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    hash_password TEXT NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone
);

DROP TABLE IF EXISTS users.auth;

CREATE TABLE IF NOT EXISTS users.auth (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    user_agent TEXT NOT NULL,
    date_time timestamp with time zone
);

DROP TABLE IF EXISTS users.refresh;

CREATE TABLE IF NOT EXISTS users.refresh (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    user_agent TEXT NOT NULL,
    refresh_token TEXT NOT NULL
);

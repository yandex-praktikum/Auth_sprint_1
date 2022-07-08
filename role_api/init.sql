BEGIN;

DROP TABLE IF EXISTS roles.roles CASCADE; 
DROP TABLE IF EXISTS roles.user_role CASCADE;


CREATE TABLE IF NOT EXISTS roles.roles (
    id UUID NOT NULL, 
    role VARCHAR NOT NULL, 
    description VARCHAR, 
    rule VARCHAR NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (id), 
    UNIQUE (role)
);

CREATE TABLE IF NOT EXISTS roles.user_role (
    user_id UUID NOT NULL, 
    role_id UUID NOT NULL, 
    PRIMARY KEY (user_id, role_id), 
    UNIQUE (role_id), 
    UNIQUE (user_id)
);

COMMIT;
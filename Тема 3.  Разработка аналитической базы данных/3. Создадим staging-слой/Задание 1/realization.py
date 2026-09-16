vertica_user = 'vt260905539720'


DROP TABLE IF EXISTS VT260905539720__STAGING.groups;
DROP TABLE IF EXISTS VT260905539720__STAGING.dialogs;
DROP TABLE IF EXISTS VT260905539720__STAGING.users;

CREATE TABLE VT260905539720__STAGING.users
(
    id              INT NOT NULL,
    chat_name       VARCHAR(200),
    registration_dt TIMESTAMP,
    country         VARCHAR(200),
    age             INT,
    CONSTRAINT pk_users PRIMARY KEY (id),
    CONSTRAINT chk_users_age CHECK (age >= 0)
)
ORDER BY id;


CREATE TABLE VT260905539720__STAGING.groups
(
    id              INT NOT NULL,
    admin_id        INT,
    group_name      VARCHAR(100),
    registration_dt TIMESTAMP,
    is_private      BOOLEAN,
    CONSTRAINT pk_groups PRIMARY KEY (id),
    CONSTRAINT fk_groups_admin
        FOREIGN KEY (admin_id)
        REFERENCES VT260905539720__STAGING.users(id)
)
order by id, admin_id
PARTITION BY registration_dt::date
GROUP BY calendar_hierarchy_day(registration_dt::date, 3, 2);


CREATE TABLE VT260905539720__STAGING.dialogs
(
    message_id      INT NOT NULL,
    message_ts      TIMESTAMP(9),
    message_from    INT,
    message_to      INT,
    message         VARCHAR(1000),
    message_group   int,
    CONSTRAINT pk_dialogs PRIMARY KEY (message_id),
    CONSTRAINT fk_dialogs_from
        FOREIGN KEY (message_from)
        REFERENCES VT260905539720__STAGING.users(id),
    CONSTRAINT fk_dialogs_to
        FOREIGN KEY (message_to)
        REFERENCES VT260905539720__STAGING.users(id),
    CONSTRAINT fk_dialogs_group
        FOREIGN KEY (message_group)
        REFERENCES VT260905539720__STAGING.groups(id)
)
ORDER BY message_id
PARTITION BY message_ts::date
GROUP BY calendar_hierarchy_day(message_ts::date, 3, 2);
drop table if exists VT260905539720.members;

create table VT260905539720.members
(
    id int PRIMARY KEY,
    age int,
    gender varchar(8),
    email varchar(256)
)
order by id
segmented by hash(id) all nodes;

copy VT260905539720.members (
    id, age, gender, email) 
from 
    local 'F:\Dev\s6-lessons\members.csv'
delimiter ';';

drop table if exists VT260905539720.dialogs;

create table VT260905539720.dialogs
(
    message_id   int PRIMARY KEY,
    message_ts   timestamp(6),
    message_from int REFERENCES members(id),
    message_to   int REFERENCES members(id),
    message      varchar(1000),
    message_group int
)
order by message_from, message_ts
segmented by hash(message_id) all nodes;

copy VT260905539720.dialogs (
    message_id, message_ts, message_from, message_to, message, message_group) 
from 
    local 'F:\Dev\s6-lessons\dialogs.csv'
delimiter ','
ENCLOSED BY '"'
ESCAPE AS '\'
SKIP 1
TRAILING NULLCOLS
REJECTED DATA AS TABLE VT260905539720.dialogs_rej;

SELECT
    u.gender,
    u.age,
    COUNT(m.message_id) AS sent
FROM VT260905539720.members AS u
INNER JOIN VT260905539720.dialogs AS m
    ON u.id = m.message_from
WHERE m.message_ts >= TRUNC(NOW(), 'DD') - '10 YEAR'::INTERVAL
GROUP BY 1, 2;
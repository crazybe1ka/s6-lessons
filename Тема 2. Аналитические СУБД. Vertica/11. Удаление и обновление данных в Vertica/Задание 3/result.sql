COPY members(id, age, gender, email ENFORCELENGTH)
FROM LOCAL 'F:\Dev\s6-lessons\members.csv'
DELIMITER ';'
REJECTED DATA AS TABLE members_rej;

CREATE TABLE members_inc LIKE members INCLUDING PROJECTIONS;

copy VT260905539720.members_inc (
    id, age, gender, email) 
FROM local 'F:\Dev\s6-lessons\members_inc.csv'
delimiter ';'

MERGE INTO members tgt /* имя таблицы в которой будут обновляться данные и в которую будут вставлены новые записи*/
USING members_inc src /*таблица или подзапрос, из которой нужно взять данные*/
ON tgt.id = src.id 
WHEN MATCHED and (
	tgt.gender IS NOT NULL AND
    tgt.email IS NOT NULL AND
    tgt.age IS NOT NULL
)
	THEN UPDATE SET 
		gender = src.gender, 
	    email = src.email, 
	    age = src.age 
WHEN NOT MATCHED
	THEN INSERT (
		id,
	    age, 
	    gender, 
	    email
	)
	VALUES (
		src.id,
	    src.age,
	    src.gender,
	    src.email
	);


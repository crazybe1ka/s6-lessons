SELECT 
	count(DISTINCT id) AS uniq,
	count(id) AS total,
	'users' AS dataset
FROM VT260905539720__STAGING.users
UNION ALL
SELECT 
	count(DISTINCT id) AS uniq,
	count(id) AS total,
	'groups' AS dataset
FROM VT260905539720__STAGING.groups
UNION ALL
SELECT 
	count(DISTINCT message_id) AS uniq,
	count(message_id) AS total,
	'dialogs' AS dataset
FROM VT260905539720__STAGING.dialogs
;
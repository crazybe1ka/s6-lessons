SELECT 
	count(DISTINCT id) AS dist_id,
	count(id) AS count_id
FROM VT260905539720__STAGING.users;
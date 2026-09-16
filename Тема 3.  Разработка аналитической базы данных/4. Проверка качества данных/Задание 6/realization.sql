SELECT count(g.admin_id)
FROM VT260905539720__STAGING.groups AS g 
JOIN VT260905539720__STAGING.users AS u 
ON g.admin_id = u.id
WHERE u.id IS NULL;
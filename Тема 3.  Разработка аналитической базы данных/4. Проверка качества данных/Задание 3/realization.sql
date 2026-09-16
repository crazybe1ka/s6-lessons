SELECT count(hash(g.group_name)), count(DISTINCT hash(g.group_name))
FROM VT260905539720__STAGING.groups g
LIMIT 10;
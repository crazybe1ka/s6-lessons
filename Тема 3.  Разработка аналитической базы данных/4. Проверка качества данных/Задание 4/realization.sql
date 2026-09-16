(SELECT 
    min(u.registration_dt) as datestamp,
    'earliest user registration' as info
FROM VT260905539720__STAGING.users u)
UNION ALL
(SELECT
    max(u.registration_dt),
    'latest user registration'
FROM VT260905539720__STAGING.users u)
UNION ALL
(SELECT 
    min(d.message_ts) as datestamp,
    'earliest dialog message' as info
FROM VT260905539720__STAGING.dialogs d)
UNION ALL
(SELECT
    max(d.message_ts),
    'latest dialog message'
FROM VT260905539720__STAGING.dialogs d)
UNION ALL
(SELECT 
    min(g.registration_dt) as datestamp,
    'earliest group creation' as info
FROM VT260905539720__STAGING.groups g)
UNION ALL
(SELECT
    max(g.registration_dt),
    'latest group creation'
FROM VT260905539720__STAGING.groups g);
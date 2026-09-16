(SELECT count(1), 'missing group admin info' as info
FROM VT260905539720__STAGING.groups g JOIN VT260905539720__STAGING.users AS u ON g.admin_id = u.id
WHERE u.id IS NULL)
UNION ALL
(SELECT COUNT(1), 'missing sender info'
FROM VT260905539720__STAGING.dialogs d JOIN VT260905539720__STAGING.users AS u ON d.message_from = u.id
WHERE u.id IS NULL)
UNION ALL
(SELECT COUNT(1), 'missing receiver info'
FROM VT260905539720__STAGING.dialogs d JOIN VT260905539720__STAGING.users AS u ON d.message_to = u.id
WHERE u.id IS NULL)
UNION ALL 
(SELECT COUNT(1), 'norm receiver info'
FROM VT260905539720__STAGING.dialogs d
WHERE d.message_to IS NULL);
SELECT
    sud.age,
    COUNT(*) AS message_count
FROM VT260905539720__DWH.l_groups_dialogs AS lgd
JOIN VT260905539720__DWH.l_user_message AS lum
    ON lgd.hk_message_id = lum.hk_message_id
JOIN VT260905539720__DWH.s_user_socdem AS sud
    ON lum.hk_user_id = sud.hk_user_id
WHERE lgd.hk_group_id IN (
    SELECT hk_group_id
    FROM VT260905539720__DWH.h_groups
    ORDER BY registration_dt
    LIMIT 10
)
GROUP BY sud.age
ORDER BY message_count DESC
LIMIT 5;
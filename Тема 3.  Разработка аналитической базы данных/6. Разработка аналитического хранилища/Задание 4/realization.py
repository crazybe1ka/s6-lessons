vertica_user = 'VT260905539720'

# INSERT INTO VT260905539720__DWH.l_admins(hk_l_admin_id, hk_group_id, hk_user_id, load_dt, load_src)
# SELECT 
# 	hash(hg.hk_group_id, hu.hk_user_id),
# 	hg.hk_group_id,
# 	hu.hk_user_id,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__STAGING.groups as g
# left join VT260905539720__DWH.h_users as hu on g.admin_id = hu.user_id
# left join VT260905539720__DWH.h_groups as hg on g.id = hg.group_id
# where hash(hg.hk_group_id, hu.hk_user_id) not in (select hk_l_admin_id from VT260905539720__DWH.l_admins);

# INSERT INTO VT260905539720__DWH.l_user_message(hk_l_user_message, hk_user_id, hk_message_id, load_dt, load_src)
# SELECT 
# 	hash(hd.hk_message_id, hu.hk_user_id),
# 	hu.hk_user_id,
# 	hd.hk_message_id,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__STAGING.dialogs as d
# left join VT260905539720__DWH.h_users as hu on d.message_from = hu.user_id
# left join VT260905539720__DWH.h_dialogs as hd on d.message_id = hd.message_id
# UNION ALL
# SELECT 
# 	hash(hd.hk_message_id, hu.hk_user_id),
# 	hu.hk_user_id,
# 	hd.hk_message_id,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__STAGING.dialogs as d
# left join VT260905539720__DWH.h_users as hu on d.message_to = hu.user_id
# left join VT260905539720__DWH.h_dialogs as hd on d.message_id = hd.message_id
# where hash(hd.hk_message_id, hu.hk_user_id) not in (select hk_l_user_message from VT260905539720__DWH.l_user_message);

# INSERT INTO VT260905539720__DWH.l_groups_dialogs(hk_l_groups_dialogs, hk_group_id, hk_message_id, load_dt, load_src)
# SELECT 
# 	hash(hd.hk_message_id, hg.hk_group_id),
# 	hg.hk_group_id,
# 	hd.hk_message_id,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__STAGING.dialogs as d
# left join VT260905539720__DWH.h_groups as hg on d.message_group = hg.group_id
# left join VT260905539720__DWH.h_dialogs as hd on d.message_id = hd.message_id
# where d.message_group IS NOT NULL AND hash(hd.hk_message_id, hg.hk_group_id) not in (select hk_l_groups_dialogs from VT260905539720__DWH.l_groups_dialogs);
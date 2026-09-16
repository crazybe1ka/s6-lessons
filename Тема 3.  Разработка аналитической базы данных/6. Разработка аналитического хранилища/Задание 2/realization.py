vertica_user = 'VT260905539720'

# INSERT INTO VT260905539720__DWH.h_users(hk_user_id, user_id, registration_dt, load_dt, load_src)
# SELECT
# 	hash(id) as hk_user_id,
# 	id as user_id,
# 	registration_dt,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__STAGING.users
# where hash(id) not in (select hk_user_id from VT260905539720__DWH.h_users);

# INSERT INTO VT260905539720__DWH.h_groups(hk_group_id, group_id,	registration_dt, load_dt, load_src)
# SELECT
# 	hash(id) as hk_group_id,
# 	id as group_id,
# 	registration_dt,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__STAGING.groups
# where hash(id) not in (select hk_group_id from VT260905539720__DWH.h_groups);

# INSERT INTO VT260905539720__DWH.h_dialogs(hk_message_id, message_id, message_ts, load_dt, load_src)
# SELECT
# 	hash(message_id) as hk_message_id,
# 	message_id,
# 	message_ts,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__STAGING.dialogs
# where hash(message_id) not in (select hk_message_id from VT260905539720__DWH.h_dialogs);
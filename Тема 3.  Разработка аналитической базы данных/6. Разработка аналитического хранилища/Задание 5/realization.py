vertica_user = 'VT260905539720'

# drop table if exists VT260905539720__DWH.s_admins;

# create table VT260905539720__DWH.s_admins
# (
# hk_admin_id bigint not null CONSTRAINT fk_s_admins_l_admins REFERENCES VT260905539720__DWH.l_admins (hk_l_admin_id),
# is_admin boolean,
# admin_from datetime,
# load_dt datetime,
# load_src varchar(20)
# )
# order by load_dt
# SEGMENTED BY hk_admin_id all nodes
# PARTITION BY load_dt::date
# GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

# INSERT INTO VT260905539720__DWH.s_admins(hk_admin_id, is_admin, admin_from, load_dt, load_src)
# SELECT 
# 	la.hk_l_admin_id,
# 	True as is_admin,
# 	hg.registration_dt,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__DWH.l_admins as la
# left join VT260905539720__DWH.h_groups as hg on la.hk_group_id = hg.hk_group_id;

# drop table if exists VT260905539720__DWH.s_user_socdem;

# create table VT260905539720__DWH.s_user_socdem
# (
# hk_user_id bigint not null CONSTRAINT fk_s_user_socdem_h_users REFERENCES VT260905539720__DWH.h_users (hk_user_id),
# country Varchar(200),
# age int,
# load_dt datetime,
# load_src varchar(20)
# )
# order by load_dt
# SEGMENTED BY hk_user_id all nodes
# PARTITION BY load_dt::date
# GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

# INSERT INTO VT260905539720__DWH.s_user_socdem(hk_user_id, country, age, load_dt, load_src)
# SELECT 
# 	hu.hk_user_id,
# 	u.country,
# 	u.age,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__DWH.h_users as hu
# left join VT260905539720__STAGING.users as u on hu.user_id = u.id;

# drop table if exists VT260905539720__DWH.s_user_chatinfo;

# create table VT260905539720__DWH.s_user_chatinfo
# (
# hk_user_id bigint not null CONSTRAINT fk_s_user_chatinfo_h_users REFERENCES VT260905539720__DWH.h_users (hk_user_id),
# chat_name Varchar(200),
# load_dt datetime,
# load_src varchar(20)
# )
# order by load_dt
# SEGMENTED BY hk_user_id all nodes
# PARTITION BY load_dt::date
# GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

# INSERT INTO VT260905539720__DWH.s_user_chatinfo(hk_user_id, chat_name, load_dt, load_src)
# SELECT 
# 	hu.hk_user_id,
# 	u.chat_name,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__DWH.h_users as hu
# left join VT260905539720__STAGING.users as u on hu.user_id = u.id;

# drop table if exists VT260905539720__DWH.s_dialog_info;

# create table VT260905539720__DWH.s_dialog_info
# (
# hk_message_id bigint not null CONSTRAINT fk_s_dialog_info_h_dialogs REFERENCES VT260905539720__DWH.h_dialogs (hk_message_id),
# message Varchar(1000),
# message_from int,
# message_to int,
# load_dt datetime,
# load_src varchar(20)
# )
# order by load_dt
# SEGMENTED BY hk_message_id all nodes
# PARTITION BY load_dt::date
# GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

# INSERT INTO VT260905539720__DWH.s_dialog_info(hk_message_id, message, message_from, message_to, load_dt, load_src)
# SELECT 
# 	hd.hk_message_id,
# 	d.message,
# 	d.message_from,
# 	d.message_to,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__DWH.h_dialogs as hd
# left join VT260905539720__STAGING.dialogs as d on hd.message_id = d.message_id;

# drop table if exists VT260905539720__DWH.s_group_name;

# create table VT260905539720__DWH.s_group_name
# (
# hk_group_id bigint not null CONSTRAINT fk_s_group_name_h_groups REFERENCES VT260905539720__DWH.h_groups (hk_group_id),
# group_name Varchar(100),
# load_dt datetime,
# load_src varchar(20)
# )
# order by load_dt
# SEGMENTED BY hk_group_id all nodes
# PARTITION BY load_dt::date
# GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

# INSERT INTO VT260905539720__DWH.s_group_name(hk_group_id, group_name, load_dt, load_src)
# SELECT 
# 	hg.hk_group_id,
# 	g.group_name,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__DWH.h_groups as hg
# left join VT260905539720__STAGING.groups as g on hg.group_id = g.id;

# drop table if exists VT260905539720__DWH.s_group_private_status;

# create table VT260905539720__DWH.s_group_private_status
# (
# hk_group_id bigint not null CONSTRAINT fk_s_group_private_status_h_groups REFERENCES VT260905539720__DWH.h_groups (hk_group_id),
# is_private boolean,
# load_dt datetime,
# load_src varchar(20)
# )
# order by load_dt
# SEGMENTED BY hk_group_id all nodes
# PARTITION BY load_dt::date
# GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);

# INSERT INTO VT260905539720__DWH.s_group_private_status(hk_group_id, is_private, load_dt, load_src)
# SELECT 
# 	hg.hk_group_id,
# 	g.is_private,
# 	now() as load_dt,
# 	's3' as load_src
# from VT260905539720__DWH.h_groups as hg
# left join VT260905539720__STAGING.groups as g on hg.group_id = g.id;

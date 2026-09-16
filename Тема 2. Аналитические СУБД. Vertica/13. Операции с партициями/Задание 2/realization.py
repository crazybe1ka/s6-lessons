vertica_user = 'vt260905539720'

# create table
#     dialogs_temp like dialogs  /*укажите название таблиц, новую и старую*/
#     including projections;

# insert into dialogs_temp
#     select 
#         message_id,
# 		message_ts,
# 		message_from,
# 		message_to,
# 		message,
# 		COALESCE(message_type, '0') /* выполнить преобразование message_type */
#     from
#         dialogs /* исходная таблица */
#     where
#         datediff('month', message_ts, now()) < 4 /* 4 неполных месяца от сегодня */;

# select
#     /* Если запрос вернёт хотя бы одну запись,
#        эта функция выдаст ошибку */
#     THROW_ERROR('Остались NULL в клоне!') as test_nulls
# from
#     dialogs_temp /* клон */
# where
#     message_type is NULL;

# SELECT
#     MIN(message_ts)::date AS min_partition,
#     MAX(message_ts)::date AS max_partition
# FROM dialogs_temp;

# select swap_partitions_between_tables(
#     'dialogs_temp', /*укажите название таблицы 1*/ 
#     '2026-06-01', /*укажите начальную партицию диапазона */
#     '2026-08-21',  /*укажите конечную партицию диапазона*/
#     'dialogs' /*укажите название таблицы 2*/
# );

# select
#     /* Если запрос вернёт хотя бы одну запись,
#        эта функция выдаст ошибку */
#     THROW_ERROR('Остались NULL в основной таблице!') as test_nulls
# from
#     dialogs /* оригинал */
# where
#     message_type is NULL
#     and datediff('month', message_ts, now()) < 4;
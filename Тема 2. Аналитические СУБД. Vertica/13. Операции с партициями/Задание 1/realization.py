vertica_user = 'vt260905539720'

# drop table if exists dialogs;

# create table dialogs 
# (
#     message_id   int PRIMARY KEY,
#     message_ts   timestamp(6) NOT NULL,
#     message_from int NOT NULL,
#     message_to   int NOT NULL,
#     message      varchar(1000),
#     message_type varchar(100)
# )
# order by 
#         message_from, message_ts
# segmented by 
#         hash(message_id) all nodes
# partition by 
#         message_ts::date
# group by 
#         calendar_hierarchy_day(message_ts::date, 3, 2)
# ;

# COPY dialogs (
#     message_id,
#     /* FILLER - означает, что в этот атрибут вектора загрузки
#     мы читаем значение из файла. Но на выход (в таблицу) оно
#     уже не поступит. Зато можно использовать message_ts_orig
#     для трансформации прямо в процессе загрузки */
#     message_ts_orig FILLER timestamp(6), 
#     message_ts as 
#         /* Поскольку данные статичны, а время идёт вперёд, 
#         для демонстрации мы сдвинем 2 последних года поближе
#         к реальному времени */
#         add_months(
#             message_ts_orig, 
#             case 
#                 when year(message_ts_orig) >= 2020 
#                 then datediff('month', '2021-06-21'::timestamp, now()::timestamp) - 1
#                 else 0
#             end
#         ),
#     message_from,
#     message_to,
#     message,
#     message_type
# )
# /* 
#     NOTE: здесь надо указать путь к файлу на вашем компьютере.
#     Для UNC путей (Windows), на забываем экранировать '\' 
#     с помощью двойного указания. Например 'C:\\Files\\dialogs.csv'
# */
# FROM LOCAL 'F:\Dev\s6-lessons\dialogs.csv' 
# DELIMITER ','
# ENCLOSED BY '"';

# SELECT DROP_PARTITIONS(
#     'dialogs', 
#     '2004-01-01', /* start partition key */
#   	'2005-12-31' /* end partition key (included) */
# );

# SELECT message_id
# FROM dialogs
# WHERE message_ts < '2005-12-31'::date;
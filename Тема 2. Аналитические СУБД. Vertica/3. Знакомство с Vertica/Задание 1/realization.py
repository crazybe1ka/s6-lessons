import vertica_python

conn_info = {'host': 'vertica.data-engineer.education-services.ru', 
             'port': '5433',
             'user': 'vt260905539720',       
             'password': 'b4565de53c9a4d3497aaf05cce6371ab',
             'database': 'dwh',
             # Вначале он нам понадобится, а дальше — решите позже сами
            'autocommit': True
}


def try_select(conn_info=conn_info):
    # И рекомендуем использовать соединение вот так
    with vertica_python.connect(**conn_info) as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 as a1;")

        res = cur.fetchall()
        return res

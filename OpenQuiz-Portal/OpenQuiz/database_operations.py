import pymysql.cursors
import time

def connect_db():

    connection = pymysql.connect(host='sql12.freesqldatabase.com',
        port=3306,
        user='sql12288801',
        password='IIRcqAD4VW',
        db='sql12288801',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)

    return connection



def generate_log(query_log):

    query = 'INSERT INTO logs(query) VALUES(%s)'
    values = (query_log,)

    conn = connect_db()
    
    with conn.cursor() as cursor:
        

        try:
            cursor.execute(query, values)
            conn.commit()
            return (True,)
        except Exception as e:
            return (False, e)

def execute_query_fetchone(query, values):

    conn = connect_db()
    
    with conn.cursor() as cursor:
        

        cursor = conn.cursor()

        try:
            cursor.execute(query, values)
            conn.commit()
            result = cursor.fetchone()
            rt = None
            if result is not None:
                rt = ()
                for data in result:
                    rt += (result[data],)
                print(rt)
            return rt
        except Exception as e:
            return e


def execute_query_many(query, values):

    conn = connect_db()
    
    with conn.cursor() as cursor:
    

        cursor.executemany(query, values)
        conn.commit()


def execute_query_fetchall(query, values):

    conn = connect_db()
    
    with conn.cursor() as cursor:
        

        cursor = conn.cursor()

        try:
            cursor.execute(query, values)
            return cursor.fetchall()
        except Exception as e:
            return e

def execute_query_get(query):

    conn = connect_db()
    
    with conn.cursor() as cursor:

        try:
            cursor.execute(query)
            result =(cursor.fetchall())
            print(result)
            rt = []
            for r in result:
                rtemp = ()
                for data in r:
                    rtemp += (r[data],)
                rt.append(rtemp)
            print(rt)
            return rt
        except Exception as e:
            print(e)
            return str(e)

def execute_query_insert(query, values):

    conn = connect_db()
    
    with conn.cursor() as cursor:
        

        cursor = conn.cursor()

        try:
            print(cursor.execute(query, values))
            conn.commit()
            return (True,)
        except Exception as e:
            return (False, e)


def get_logs():

    query = 'SELECT * FROM logs;'
    result = execute_query_fetchall(query, ())
    return result



def dict_to_list(dic):

    l = []
    for row in dic:
        t = ()
        for key in row:
            t += (row[key],)
        l.append(t)

    return l 
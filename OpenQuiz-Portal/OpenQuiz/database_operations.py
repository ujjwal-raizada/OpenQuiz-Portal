import sqlite3
import time

def generate_log(query_log):

    query = 'INSERT INTO logs(query) VALUES(?)'
    values = (query_log,)

    conn = sqlite3.connect('quiz-portal.db', check_same_thread=False)
    conn.execute('PRAGMA foreign_keys = 1')

    cursor = conn.cursor()

    try:
        cursor.execute(query, values)
        conn.commit()
        return (True,)
    except Exception as e:
        return (False, e)

def execute_query_fetchone(query, values):

    conn = sqlite3.connect('quiz-portal.db', check_same_thread=False)
    conn.execute('PRAGMA foreign_keys = 1')
    conn.set_trace_callback(generate_log)

    cursor = conn.cursor()

    try:
        cursor.execute(query, values)
        conn.commit()
        return cursor.fetchone()
    except Exception as e:
        return e


def execute_query_many(query, values):

    conn = sqlite3.connect('quiz-portal.db', check_same_thread=False)
    conn.execute('PRAGMA foreign_keys = 1')
    conn.set_trace_callback(generate_log)

    cursor = conn.cursor()

    cursor.executemany(query, values)
    conn.commit()


def execute_query_fetchall(query, values):

    conn = sqlite3.connect('quiz-portal.db', check_same_thread=False)
    conn.execute('PRAGMA foreign_keys = 1')
    conn.set_trace_callback(generate_log)

    cursor = conn.cursor()

    try:
        cursor.execute(query, values)
        return cursor.fetchall()
    except Exception as e:
        return e

def execute_query_get(query):

    conn = sqlite3.connect('quiz-portal.db', check_same_thread=False)
    conn.execute('PRAGMA foreign_keys = 1')
    conn.set_trace_callback(generate_log)

    cursor = conn.cursor()


    try:
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        return str(e)

def execute_query_insert(query, values):

    conn = sqlite3.connect('quiz-portal.db', check_same_thread=False)
    conn.execute('PRAGMA foreign_keys = 1')
    conn.set_trace_callback(generate_log)

    cursor = conn.cursor()

    try:
        cursor.execute(query, values)
        conn.commit()
        return (True,)
    except Exception as e:
        return (False, e)


def get_logs():

    query = 'SELECT * FROM logs;'
    result = execute_query_fetchall(query, ())
    return result
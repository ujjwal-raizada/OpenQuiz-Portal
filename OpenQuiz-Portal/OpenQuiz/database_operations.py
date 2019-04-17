import sqlite3
import time

conn = sqlite3.connect('quiz-portal.db')
conn.execute('PRAGMA foreign_keys = 1')

cursor = conn.cursor()


def execute_query_fetchone(query, values):

    try:
        cursor.execute(query, values)
        return cursor.fetchone()
    except Exception as e:
        return e

def execute_query_fetchall(query, values):

    try:
        cursor.execute(query, values)
        return cursor.fetchall()
    except Exception as e:
        return e

def execute_query_get(query):

    try:
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        return str(e)

def execute_query_insert(query, values):

    try:
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        return str(e)

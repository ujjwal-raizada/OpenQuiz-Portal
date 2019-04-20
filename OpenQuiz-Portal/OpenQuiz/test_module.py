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
        return (True,)
    except Exception as e:
        return (False, e)



def insert_faculty_in_course(fid, cid):

    query = 'INSERT into facultycourse(fid, cid) VALUES(%s, %s)'
    values = (fid, cid)
    result = execute_query_insert(query, values)
    return result


def insert_student_in_course(sid, cid):

    query = 'INSERT into studentcourse(sid, cid) VALUES(%s, %s)'
    values = (sid, cid)
    result = execute_query_insert(query, values)
    return result

print(insert_faculty_in_course(1, 'cs f212'))
print(insert_student_in_course('2017A7PS1398H', 'cs f212'))
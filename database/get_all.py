import sqlite3

conn = sqlite3.connect('quiz-portal.db')
conn.execute('PRAGMA foreign_keys = 1')

cursor = conn.cursor()

def execute_query_get(query):

    try:
        cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        return str(e)


def get_all_course():
    query = 'SELECT * FROM [course];'
    return list(execute_query_get(query))

def get_all_student():
    query = 'SELECT * FROM [student];'
    return list(execute_query_get(query))

def get_all_faculty():
    query = 'SELECT * FROM [faculty];'
    return list(execute_query_get(query))

def get_all_quiz():
    query = 'SELECT * FROM [quiz];'
    return list(execute_query_get(query))

def get_all_problem():
    query = 'SELECT * FROM [problem];'
    return list(execute_query_get(query))

def get_all_studentcourse():
    query = 'SELECT * FROM [studentcourse];'
    return list(execute_query_get(query))

def get_all_facultycourse():
    query = 'SELECT * FROM [facultycourse];'
    return list(execute_query_get(query))

def get_all_response():
    query = 'SELECT * FROM [response];'
    return list(execute_query_get(query))

def get_all_marklist():
    query = 'SELECT * FROM [marklist];'
    return list(execute_query_get(query))

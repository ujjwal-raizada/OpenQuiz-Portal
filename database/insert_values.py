import sqlite3

conn = sqlite3.connect('quiz-portal.db')
conn.execute('PRAGMA foreign_keys = 1')

cursor = conn.cursor()


def execute_query_insert(query, values):

    try:
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        return str(e)


def create_faculty(fname, dept):
    
    query = 'INSERT INTO faculty(fname, dept) VALUES(?, ?)'
    values = (fname, dept)
    return execute_query_insert(query, values)


def create_student(sid, sname):

    # TODO: Use regex for ID
    
    query = 'INSERT INTO student(sid, sname) VALUES(?, ?)'
    values = (sid, sname)
    return execute_query_insert(query, values)


def create_course(cid, cname, ic_id):

    # TODO: Use regex for Course ID

    query = 'INSERT INTO course(cid, cname, ic_id) VALUES(?, ?, ?)'
    values = (cid, cname, ic_id)
    return execute_query_insert(query, values)


def create_quiz(fid, cid, qname, start, end):
    
    query = 'INSERT INTO quiz(fid, cid, qname, start, end) VALUES(?, ?, ?, ?, ?)'
    values = (fid, cid, qname, start, end)
    return execute_query_insert(query, values)


def create_problem(qid, statement, op1, op2, op3, op4, ans, positive, negative):

    query = '''
    INSERT INTO problem(qid, statement, option1, option2, option3, option4, ans, positive, negative)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    values = qid, statement, op1, op2, op3, op4, ans, positive, negative
    return execute_query_insert(query, values)

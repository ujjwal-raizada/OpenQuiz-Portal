import sqlite3
conn = sqlite3.connect('quiz-portal.db')
conn.execute('PRAGMA foreign_keys = 1')

cursor = conn.cursor()

def execute_query(query):

    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        return str(e)

def createFacultyTable():
    query = """
    CREATE TABLE IF NOT EXISTS faculty (
        fid INTEGER PRIMARY KEY,
        fname TEXT,
        dept TEXT
    );
    """
    return execute_query(query)

def createCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS course (
        cid TEXT PRIMARY KEY,
        cname TEXT,
        ic_id INTEGER,
        FOREIGN KEY (ic_id) REFERENCES faculty(fid)
    );
    """
    return execute_query(query)

def createQuizTable():
    query = """
    CREATE TABLE IF NOT EXISTS quiz (
        qid INTEGER PRIMARY KEY,
        fid INTEGER,
        cid TEXT,
        qname TEXT,
        start TEXT,
        end TEXT,
        FOREIGN KEY (fid) REFERENCES faculty(fid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    return execute_query(query)

def createProblemTable():
    query = """
    CREATE TABLE IF NOT EXISTS problem (
        pid INTEGER PRIMARY KEY,
        qid INTEGER,
        statement TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        ans TEXT,
        positive INTEGER,
        negative INTEGER,
        FOREIGN KEY (qid) REFERENCES quiz(qid)

    );
    """
    return execute_query(query)

def createStudentTable():
    query = """
    CREATE TABLE IF NOT EXISTS student (
        sid TEXT PRIMARY KEY,
        sname TEXT
    );
    """
    return execute_query(query)

def createFacultyCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS facultycourse (
        fid INTEGER,
        cid TEXT,
        FOREIGN KEY (fid) REFERENCES faculty(fid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    return execute_query(query)

def createStudentCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS studentcourse (
        sid TEXT,
        cid TEXT,
        FOREIGN KEY (sid) REFERENCES student(sid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    return execute_query(query)


def createResponseTable():
    query = """
    CREATE TABLE IF NOT EXISTS response (
        sid TEXT,
        pid INTEGER,
        qid INTEGER,
        option TEXT,
        FOREIGN KEY (sid) REFERENCES student(sid),
        FOREIGN KEY (qid) REFERENCES quiz(qid),
        FOREIGN KEY (pid) REFERENCES problem(pid)
    );
    """
    return execute_query(query)

def createMarklistTable():
    query = """
    CREATE TABLE IF NOT EXISTS marklist (
        qid INTEGER,
        sid INTEGER,
        marks INTEGER,
        FOREIGN KEY (sid) REFERENCES student(sid),
        FOREIGN KEY (qid) REFERENCES quiz(qid)
    );
    """
    return execute_query(query)


createCourseTable()
createFacultyTable()
createFacultyCourseTable()
createMarklistTable()
createProblemTable()
createQuizTable()
createResponseTable()
createStudentCourseTable()
createStudentTable()

conn.close()

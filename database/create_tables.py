import sqlite3
conn = sqlite3.connect('quiz-portal.db')

cursor = conn.cursor()

def execute_query(query):

    cursor.execute(query)
    conn.commit()

def createFacultyTable():
    query = """
    CREATE TABLE IF NOT EXISTS faculty (
        fid INTEGER PRIMARY KEY,
        fname TEXT,
        dept TEXT
    );
    """
    execute_query(query)

def createCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS course (
        cid TEXT PRIMARY KEY,
        cname TEXT,
        ic_id TEXT,
        FOREIGN KEY (ic_id) REFERENCES faculty(fid)
    );
    """
    execute_query(query)

def createQuizTable():
    query = """
    CREATE TABLE IF NOT EXISTS quiz (
        qid INTEGER PRIMARY KEY,
        fid INTEGER,
        cid TEXT,
        qname TEXT,
        start TIMESTAMP,
        end TIMESTAMP,
        FOREIGN KEY (fid) REFERENCES faculty(fid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    execute_query(query)

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
        postive INTEGER,
        negative INTEGER,
        FOREIGN KEY (qid) REFERENCES quiz(qid)

    );
    """
    execute_query(query)

def createStudentTable():
    query = """
    CREATE TABLE IF NOT EXISTS student (
        sid TEXT PRIMARY KEY,
        sname TEXT
    );
    """
    execute_query(query)

def createFacultyCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS facultycourse (
        fid INTEGER,
        cid TEXT,
        FOREIGN KEY (fid) REFERENCES faculty(fid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    execute_query(query)

def createStudentCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS studentcourse (
        sid TEXT,
        cid TEXT,
        FOREIGN KEY (sid) REFERENCES student(sid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    execute_query(query)


def createResponseTable():
    query = """
    CREATE TABLE IF NOT EXISTS response (
        sid TEXT,
        pid INTEGER,
        option TEXT,
        FOREIGN KEY (sid) REFERENCES student(sid),
        FOREIGN KEY (pid) REFERENCES problem(pid)
    );
    """
    execute_query(query)

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
    execute_query(query)


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

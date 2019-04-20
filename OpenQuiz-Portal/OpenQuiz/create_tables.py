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




def execute_query(query):

    conn = connect_db()
    
    with conn.cursor() as cursor:
        try:
            cursor.execute(query)
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return str(e)


def createFacultyTable():
    query = """
    CREATE TABLE IF NOT EXISTS faculty (
        fid INTEGER PRIMARY KEY AUTO_INCREMENT,
        fname varchar(30),
        email varchar(30) UNIQUE,
        dept varchar(30)
    );
    """
    return execute_query(query)

def createCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS course (
        cid varchar(30) PRIMARY KEY,
        cname varchar(30),
        ic_id INTEGER,
        FOREIGN KEY (ic_id) REFERENCES faculty(fid)
    );
    """
    return execute_query(query)

def createQuizTable():
    query = """
    CREATE TABLE IF NOT EXISTS quiz (
        qid INTEGER PRIMARY KEY AUTO_INCREMENT,
        fid INTEGER,
        cid varchar(30),
        qname varchar(30),
        start varchar(30),
        end varchar(30),
        FOREIGN KEY (fid) REFERENCES faculty(fid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    return execute_query(query)

def createProblemTable():
    query = """
    CREATE TABLE IF NOT EXISTS problem (
        pid INTEGER PRIMARY KEY AUTO_INCREMENT,
        qid INTEGER,
        statement varchar(30),
        option1 varchar(2),
        option2 varchar(2),
        option3 varchar(2),
        option4 varchar(2),
        ans varchar(2),
        positive INTEGER,
        negative INTEGER,
        FOREIGN KEY (qid) REFERENCES quiz(qid)

    );
    """
    return execute_query(query)

def createStudentTable():
    query = """
    CREATE TABLE IF NOT EXISTS student (
        sid varchar(30) PRIMARY KEY,
        sname varchar(30)
    );
    """
    return execute_query(query)

def createFacultyCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS facultycourse (
        fid INTEGER,
        cid varchar(30),
        FOREIGN KEY (fid) REFERENCES faculty(fid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    return execute_query(query)

def createStudentCourseTable():
    query = """
    CREATE TABLE IF NOT EXISTS studentcourse (
        sid varchar(30),
        cid varchar(30),
        FOREIGN KEY (sid) REFERENCES student(sid),
        FOREIGN KEY (cid) REFERENCES course(cid)
    );
    """
    return execute_query(query)


def createResponseTable():
    query = """
    CREATE TABLE IF NOT EXISTS response (
        sid varchar(30),
        pid INTEGER,
        qid INTEGER,
        option1 varchar(2),
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
        sid varchar(30),
        marks INTEGER,
        FOREIGN KEY (sid) REFERENCES student(sid),
        FOREIGN KEY (qid) REFERENCES quiz(qid)
    );
    """
    return execute_query(query)

def createLogsTable():

    query = '''
    CREATE TABLE IF NOT EXISTS logs (
        query varchar(30),
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    '''
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
createLogsTable()

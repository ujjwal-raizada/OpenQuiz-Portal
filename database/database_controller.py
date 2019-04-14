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


def is_student(sid):

    query = 'SELECT sid from student where sid = ?;'
    values = (sid,)
    result = execute_query_fetchone(query, values)
    if (result is not None):
        return True
    else:
        return False

def is_Student_in_course(sid, cid):

    query = 'SELECT sid, cid FROM studentcourse WHERE sid = ? AND cid = ?;'
    values = (sid, cid)
    result = execute_query_fetchone(query, values)
    if (result is not None):
        return True
    else:
        return False

def is_faculty_in_course(fid, cid):

    query = 'SELECT fid, cid FROM facultycourse WHERE fid = ? AND cid = ?;'
    values = (fid, cid)
    result = execute_query_fetchone(query, values)
    if (result is not None):
        return True
    else:
        return False


def quiz_status(qid):

    query = 'select start, end from quiz WHERE qid = ?;'
    values = (qid,)
    result = execute_query_fetchone(query, values)
    current_time = time.time()

    start = float(result[0])
    end = float(result[1]) + 10  # 10 seconds bonus!

    if (current_time >= start and current_time <= end):
        return (True, 'Quiz is running!')
    elif (current_time < start):
        return (False, 'Quiz not started yet!')
    else:
            return (False, 'Quiz ended!')


def is_student_in_quiz(sid, qid):

    query = '''
    SELECT * from student, studentcourse, quiz
    where student.sid = studentcourse.sid AND studentcourse.cid = quiz.cid
    AND student.sid = ? AND quiz.qid = ?;
    '''
    values = (sid, qid)
    result = execute_query_fetchone(query, values)
    if (result is not None):
        return True
    else:
        return False

def get_problems(qid):

    query = 'SELECT * FROM problem WHERE qid = ?;'
    values = (qid,)
    result = execute_query_fetchall(query, values)
    print(result)
    
    problems = []

    for problem in result:
        p = {
            'pid': problem[0],
            'statement': problem[2],
            'option1': problem[3],
            'option2': problem[4],
            'option3': problem[5],
            'option4': problem[6],
            'positive': problem[8],
            'negative': problem[9],
        }
        problems.append(p)

    return problems

def no_of_ques(qid):

    query = 'SELECT count(*) FROM problem WHERE qid = ? GROUP BY qid;'
    values = (qid,)
    return execute_query_fetchone(query, values)[0]


def insert_response(qid, sid, response):

    # [(pid, option)]
    no_ques = no_of_ques(qid)

    # check if all question are submitted
    if (no_ques != len(response)):
        return False
    

    query = []
    for ans in response:
        query.append((sid, ans[0], qid, ans[1]))

    try:
        cursor.executemany('INSERT INTO response VALUES (?, ?, ?, ?)', query)
        conn.commit()
        return True
    except Exception:
        return False


def calculate_marks(sid, qid):

    # Find correct answers
    query = 'SELECT pid, ans, positive, negative FROM problem WHERE qid = ?;'
    values = (qid,)
    result1 = execute_query_fetchall(query, values)

    # Get the responses
    query = 'SELECT pid, option FROM response WHERE sid = ? AND qid = ?;'
    values = (sid, qid)
    result2 = execute_query_fetchall(query, values)

    # match the answers:
    result1.sort()
    result2.sort()
    marks = 'Not Attempted.'

    if (len(result1) == len(result2)):
        marks = 0
        for i in range(len(result1)):
            if (result1[i][1] == result2[i][1]):
                marks += result1[i][2]
            else:
                marks -= result1[i][3]

    return marks


def generate_mark_list(qid):
     
    # get student list
    query = 'SELECT sid FROM studentcourse, quiz WHERE studentcourse.cid = quiz.cid AND qid = ?;'
    values = (qid,)
    result = execute_query_fetchall(query, values)
     
    quiz_report = []

    for student in result:
        marks = calculate_marks(student[0], qid)
        quiz_report.append((student[0], marks))

    return quiz_report




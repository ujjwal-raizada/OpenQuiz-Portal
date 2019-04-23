import time
from .database_operations import execute_query_fetchall, execute_query_fetchone
from .database_operations import execute_query_get, execute_query_insert, execute_query_many
from .database_operations import dict_to_list


class Quiz:

    @staticmethod
    def create_quiz(fid, cid, qname, start, end):
        
        query = 'INSERT INTO quiz(fid, cid, qname, start, end) VALUES(%s, %s, %s, %s, %s)'
        values = (fid, cid, qname, start, end)
        return execute_query_insert(query, values)

    @staticmethod
    def create_problem(qid, statement, op1, op2, op3, op4, ans, positive, negative):

        query = '''
        INSERT INTO problem(qid, statement, option1, option2, option3, option4, ans, positive, negative)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        values = qid, statement, op1, op2, op3, op4, ans, positive, negative
        return execute_query_insert(query, values)

    @staticmethod
    def get_all_quiz():
        query = 'SELECT * FROM quiz;'
        return list(execute_query_get(query))

    @staticmethod
    def get_all_problem():
        query = 'SELECT * FROM problem;'
        return list(execute_query_get(query))

    @staticmethod
    def get_all_response():
        query = 'SELECT * FROM response;'
        return list(execute_query_get(query))

    @staticmethod
    def get_all_marklist():
        query = 'SELECT * FROM marklist;'
        return list(execute_query_get(query))

    @staticmethod
    def quiz_status(qid):

        query = 'select start, end from quiz WHERE qid = %s;'
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

    @staticmethod
    def is_student_in_quiz(sid, qid):

        query = '''
        SELECT * from student, studentcourse, quiz
        where student.sid = studentcourse.sid AND studentcourse.cid = quiz.cid
        AND student.sid = %s AND quiz.qid = %s;
        '''
        values = (sid, qid)
        result = execute_query_fetchone(query, values)
        if (result is not None):
            return True
        else:
            return False
    @staticmethod
    def get_problems(qid):

        query = 'SELECT * FROM problem WHERE qid = %s;'
        values = (qid,)
        result = execute_query_fetchall(query, values)
        # print(result)
        
        problems = []

        for problem in result:
            p = {
                'pid': problem['pid'],
                'statement': problem['statement'],
                'option1': problem['option1'],
                'option2': problem['option2'],
                'option3': problem['option3'],
                'option4': problem['option4'],
                'positive': problem['positive'],
                'negative': problem['negative'],
            }
            problems.append(p)

        return problems

    @staticmethod
    def no_of_ques(qid):

        query = 'SELECT count(*) FROM problem WHERE qid = %s GROUP BY qid;'
        values = (qid,)
        return execute_query_fetchone(query, values)[0]

    @staticmethod
    def insert_response(qid, sid, response):

        # [(pid, option)]
        no_ques = Quiz.no_of_ques(qid)

        # check if all question are submitted
        if (no_ques != len(response)):
            return False
        

        values = []
        for ans in response:
            values.append((sid, ans[0], qid, ans[1]))

        try:

            query = 'INSERT INTO response(sid, pid, qid, option1) VALUES (%s, %s, %s, %s)'
            for value in values:
                print(value)
                execute_query_insert(query, value)

            return True
        except Exception:
            return False

    @staticmethod
    def calculate_marks(sid, qid):

        # Find correct answers
        query = 'SELECT pid, ans, positive, negative FROM problem WHERE qid = %s;'
        values = (qid,)
        result1 = execute_query_fetchall(query, values)

        # Get the responses
        query = 'SELECT pid, option1 FROM response WHERE sid = %s AND qid = %s;'
        values = (sid, int(qid))
        result2 = execute_query_fetchall(query, values)

        result2 = dict_to_list(result2)
        result1 = dict_to_list(result1)
        
        # print(result1)
        # print(result2)


        # match the answers:
        result1.sort()
        result2.sort()
        marks = 'Not Attempted.'

        if (len(result1) == len(result2)):
            marks = 0
            for i in range(len(result1)):
                if (result1[i][1] == result2[i][1] and result2[i][1] != 'E'):
                    marks += result1[i][2]
                else:
                    marks -= result1[i][3]

        return marks

    @staticmethod
    def generate_mark_list(qid):
        
        # get student list
        query = 'SELECT sid FROM studentcourse, quiz WHERE studentcourse.cid = quiz.cid AND qid = %s;'
        values = (qid,)
        result = execute_query_fetchall(query, values)
        
        quiz_report = []

        for student in result:
            marks = Quiz.calculate_marks(student['sid'], qid)
            quiz_report.append((student['sid'], marks))

        return quiz_report

    @staticmethod
    def get_faculty_quiz(fid):

        query = 'SELECT qid, cid, qname FROM quiz WHERE fid=%s;'
        values = (fid,)

        result = execute_query_fetchall(query, values)
        return result


    @staticmethod
    def quiz_attempted(qid, sid):

        marks = Quiz.calculate_marks(sid, qid)

        if (marks == 'Not Attempted.'):
            return False
        else:
            return True


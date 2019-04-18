import time
from .database_operations import execute_query_fetchall, execute_query_fetchone
from .database_operations import execute_query_get, execute_query_insert


class Course:

    @staticmethod
    def create_course(cid, cname, ic_id):

        # TODO: Use regex for Course ID

        query = 'INSERT INTO course(cid, cname, ic_id) VALUES(?, ?, ?)'
        values = (cid, cname, ic_id)
        return execute_query_insert(query, values)

    @staticmethod
    def get_all_course():
        query = 'SELECT * FROM [course];'
        return list(execute_query_get(query))

    @staticmethod
    def get_all_facultycourse():
        query = 'SELECT * FROM [facultycourse];'
        return list(execute_query_get(query))

    @staticmethod
    def get_all_studentcourse():
        query = 'SELECT * FROM [studentcourse];'
        return list(execute_query_get(query))

    @staticmethod
    def is_Student_in_course(sid, cid):

        query = 'SELECT sid, cid FROM studentcourse WHERE sid = ? AND cid = ?;'
        values = (sid, cid)
        result = execute_query_fetchone(query, values)
        if (result is not None):
            return True
        else:
            return False

    @staticmethod
    def is_faculty_in_course(fid, cid):

        query = 'SELECT fid, cid FROM facultycourse WHERE fid = ? AND cid = ?;'
        values = (fid, cid)
        result = execute_query_fetchone(query, values)
        if (result is not None):
            return True
        else:
            return False

    @staticmethod
    def insert_faculty_in_course(fid, cid):

        query = 'INSERT into facultycourse(fid, cid) VALUES(?, ?)'
        values = (fid, cid)
        result = execute_query_insert(query, values)
        return result

    @staticmethod
    def insert_student_in_course(sid, cid):

        query = 'INSERT into studentcourse(sid, cid) VALUES(?, ?)'
        values = (sid, cid)
        result = execute_query_insert(query, values)
        return result

    @staticmethod
    def is_course(cid):

        query = 'SELECT cid from course where cid = ?;'
        values = (cid,)
        result = execute_query_fetchone(query, values)
        if (result is not None):
            return True
        else:
            return False

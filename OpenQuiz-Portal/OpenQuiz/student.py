import time
from .database_operations import execute_query_fetchall, execute_query_fetchone
from .database_operations import execute_query_get, execute_query_insert


class Student:

    @staticmethod
    def create_student(sid, sname):

        # TODO: Use regex for ID
        
        query = 'INSERT INTO student(sid, sname) VALUES(%s, %s)'
        values = (sid, sname)
        return execute_query_insert(query, values)

    @staticmethod
    def get_all_student():
        query = 'SELECT * FROM student;'
        return list(execute_query_get(query))

    @staticmethod
    def is_student(sid):

        query = 'SELECT sid from student where sid = %s;'
        values = (sid,)
        result = execute_query_fetchone(query, values)
        if (result is not None):
            return True
        else:
            return False
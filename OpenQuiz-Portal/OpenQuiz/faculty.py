import time
from .database_operations import execute_query_fetchall, execute_query_fetchone
from .database_operations import execute_query_get, execute_query_insert


class Faculty:

    @staticmethod
    def create_faculty(fname, email, dept):
        
        query = 'INSERT INTO faculty(fname, email, dept) VALUES(?, ?, ?)'
        values = (fname, email, dept)
        return execute_query_insert(query, values)

    @staticmethod
    def get_all_faculty():
        query = 'SELECT * FROM [faculty];'
        return list(execute_query_get(query))

    @staticmethod
    def is_faculty(fid):

        query = 'SELECT fid from faculty where fid = ?;'
        values = (fid,)
        result = execute_query_fetchone(query, values)
        if (result is not None):
            return True
        else:
            return False
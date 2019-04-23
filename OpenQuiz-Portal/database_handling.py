import time
from OpenQuiz.student import Student
from OpenQuiz.quiz import Quiz
from OpenQuiz.course import Course
from OpenQuiz.faculty import Faculty
from OpenQuiz.database_operations import get_logs

# print(Student.create_student('2017A7PS1398H', 'Ujjwal Raizada'))
# print(Student.create_student('2017A7PS0277H', 'Satyam Mani'))
# print(Student.create_student('2017A7PS1715H', 'Prakhar Goenka'))
# print(Student.create_student('2017A7PS0218H', 'Daksh Yashlaha'))

# print(Faculty.create_faculty('Lov Kumar', 'lov@hyderabad.bits-pilani.ac.in', 'CS'))
# print(Faculty.create_faculty('T. Ray', 'rayt', 'CS'))
# print(Faculty.create_faculty('NL Bhanu Murty','bhanu', 'CS'))
# print(Faculty.create_faculty('PKT','pkt@hyderabad.bits-pilani.ac.in', 'PHY'))

# Course.create_course('CS F211', 'DSA', 3)
# Course.create_course('CS F212', 'DBMS', 1)
# Course.create_course('PHY F111', 'PHYSICS', 4)

# Quiz.create_quiz(3, 'CS F211', 'Graph', time.time(), time.time() + 600)
# Quiz.create_quiz(1, 'CS F212', 'SQL Queries', time.time(), time.time() + 600)
# Quiz.create_quiz(1, 'CS F212', 'SQL Queries 2', time.time(), time.time() + 600)


# print(Quiz.create_problem(1, 'Number of edges in a tree%s', 'n', 'n - 1', 'n + 1', '2n', 'B', 3, 1))
# print(Quiz.create_problem(1, 'Number of edges in a single cycle%s', 'n', 'n - 1', 'n + 1', '2n', 'A', 3, 1))
# print(Quiz.create_problem(1, 'Number of edges in a single node graph%s', 'n', '0', 'n + 1', '2n', 'B', 3, 1))

# A = [
#     (1, 'A'),
#     (2, 'A'),
#     (3, 'B'),
# ]

# print(Quiz.insert_response(1, '2017A7PS1398H', A))

# print(Course.insert_student_in_course('2017A7PS1398H', 'CS F211'))
# print(Course.insert_student_in_course('2017A7PS0277H', 'CS F212'))

# print(Course.insert_faculty_in_course(3, 'CS F211'))
# print(Course.insert_faculty_in_course(1, 'CS F212'))

# print(Quiz.generate_mark_list(1))

# print(get_logs())

print(Quiz.quiz_attempted(1, '2017A7PS1398H'))
import time
from insert_values import create_course, create_faculty, create_problem, create_quiz, create_student

create_student('2017A7PS1398H', 'Ujjwal Raizada')
create_student('2017A7PS0277H', 'Satyam Mani')
create_student('2017A7PS1715H', 'Prakhar Goenka')
create_student('2017A7PS0218H', 'Daksh Yashlaha')

create_faculty('Lov Kumar', 'CS')
create_faculty('T. Ray', 'CS')
create_faculty('NL Bhanu Murty', 'CS')
create_faculty('PKT', 'PHY')

create_course('CS F211', 'DSA', 3)
create_course('CS F212', 'DBMS', 1)
create_course('PHY F111', 'PHYSICS', 4)

create_quiz(3, 'CS F211', 'Graph', time.time(), time.time() + 600)
create_quiz(1, 'CS F212', 'SQL Queries', time.time(), time.time() + 600)


print(create_problem(1, 'Number of edges in a tree?', 'n', 'n - 1', 'n + 1', '2n', 'B', 3, 1))
print(create_problem(1, 'Number of edges in a single cycle?', 'n', 'n - 1', 'n + 1', '2n', 'A', 3, 1))
print(create_problem(1, 'Number of edges in a single node graph?', 'n', '0', 'n + 1', '2n', 'B', 3, 1))





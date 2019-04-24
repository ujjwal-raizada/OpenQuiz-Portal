import os
import datetime
from OpenQuiz.student import Student
from OpenQuiz.faculty import Faculty
from OpenQuiz.quiz import Quiz
from OpenQuiz.course import Course
from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationFormStudent, RegistrationFormFaculty
from app.forms import CourseForm, StudentCourseForm, FacultyCourseForm, GetProblems
from app.forms import CreateProblem, CreateQuiz, QuizForm, GetResult
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():

  print(os.getcwd()) 
  return render_template('index.html', title='Home', user_type = current_user.user_type)

@app.route('/login', methods=['GET', 'POST'])
def login():

  if current_user.is_authenticated:
    return redirect(url_for('index'))

  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data).first()

    if user is None or not user.check_password(form.password.data):
      flash('Invalid email or password')
      return redirect(url_for('login'))

    login_user(user, remember = form.remember_me.data)
    next_page = request.args.get('next')

    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)

  return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():

  logout_user()
  return redirect(url_for('index'))

@app.route('/register/student', methods=['GET', 'POST'])
def registerStudent():

  if current_user.is_authenticated:
    return redirect(url_for('index'))

  form = RegistrationFormStudent()

  if form.validate_on_submit():
    Student.create_student(form.studentid.data, form.name.data)
    user = User(username = form.username.data, email = form.email.data, 
                user_id = form.studentid.data, user_type = 'Student')
    user.set_password(form.password.data)

    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered student!')    
    return redirect(url_for('login'))

  return render_template('registerStudent.html', title = 'Register Student', form = form)

@app.route('/register/faculty', methods=['GET', 'POST'])
def registerFaculty():

  if current_user.is_authenticated:
    return redirect(url_for('index'))

  form = RegistrationFormFaculty()

  if form.validate_on_submit():
    print(Faculty.create_faculty(form.name.data, form.email.data, form.department.data))
    user = User(username = form.username.data, email = form.email.data, 
                user_id = 'Null', user_type = 'Faculty')
    user.set_password(form.password.data)

    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered faculty!')
    return redirect(url_for('login'))

  return render_template('registerFaculty.html', title = 'Register Faculty', form = form)

@app.route('/addcourse', methods=['GET', 'POST'])
@login_required
def addcourse():

  form = CourseForm()
  form.ic_id.choices = [(str(i[0]), i[1]) for i in Faculty.get_all_faculty()]

  if form.validate_on_submit():
    Course.create_course(form.course_id.data, form.course_name.data, int(form.ic_id.data)) 
    flash('The course has been added successfully')
    return redirect(url_for('index'))

  return render_template('courseForm.html', title = 'Add Course', form = form)

@app.route('/studentcourse', methods=['GET', 'POST'])
@login_required
def studentcourse():

  form = StudentCourseForm()
  form.course.choices = [(course[0], course[1]) for course in Course.get_all_course()]

  if form.validate_on_submit():
    temp = Course.is_Student_in_course(current_user.user_id, form.course.data)

    if temp:
      flash('The student is already enrolled in the course')
    else:
      Course.insert_student_in_course(current_user.user_id, form.course.data)
      flash('The student has been successfully enrolled in the course')
    return redirect(url_for('index'))

  return render_template('studentCourse.html', title = 'Enroll Course', form = form)

@app.route('/facultycourse', methods=['GET', 'POST'])
@login_required
def facultycourse():

  form = FacultyCourseForm()
  form.course.choices = [(course[0], course[1]) for course in Course.get_all_course()] 

  if form.validate_on_submit():
    faculty_id = (Faculty.get_faculty_id(current_user.email))

    if faculty_id[0] == False:
      flash('Error: Faculty not registered in the database')
    else:
      Course.insert_faculty_in_course(faculty_id[1], form.course.data)
      flash('The faculty has been successfully enrolled in the course')
      return redirect(url_for('index'))
      
  return render_template('facultyCourse.html', title = 'Enroll Course', form = form)

@app.route('/createquiz', methods=['GET', 'POST'])
@login_required
def createquiz():

  faculty_id = Faculty.get_faculty_id(current_user.email)[1]
  courses = Faculty.get_faculty_course(faculty_id)

  form = CreateQuiz()
  form.course.choices = [(course['cid'], course['cid']) for course in courses]

  if form.validate_on_submit():  
    a, b, c, d, e, f = map(int, form.start_time.data.split())
    start_time = datetime.datetime(a, b, c, d, e, f).timestamp()
    a, b, c, d, e, f = map(int, form.end_time.data.split())
    end_time = datetime.datetime(a, b, c, d, e, f).timestamp()
    Quiz.create_quiz(faculty_id, form.course.data, form.quiz_name.data,
     start_time, end_time)
    flash('Quiz created successfully')
    return redirect(url_for('index'))

  return render_template('createQuiz.html', title = 'Create Quiz', form = form)

@app.route('/createproblem', methods=['GET', 'POST'])
@login_required
def createproblem():

  faculty_id = Faculty.get_faculty_id(current_user.email)[1]
  quizes = Quiz.get_faculty_quiz(faculty_id)

  form = CreateProblem()
  form.quiz_id.choices = [(str(quiz['qid']), "{}: {}".format(quiz['cid'], quiz['qname']))\
   for quiz in quizes]

  if form.validate_on_submit():
    Quiz.create_problem(form.quiz_id.data,form.statement.data, form.op_1.data, form.op_2.data,
     form.op_3.data, form.op_4.data, form.ans.data, form.positive.data, form.negative.data)
    flash('problem created successfully')
    return redirect(url_for('index'))

  return render_template('createProblem.html', title = 'Create Problem', form = form)

@app.route('/getproblems', methods=['GET', 'POST'])
@login_required
def getproblems():

  faculty_id = Faculty.get_faculty_id(current_user.email)[1]
  quizes = Quiz.get_faculty_quiz(faculty_id)

  form = GetProblems()
  form.quiz_id.choices = [(str(quiz['qid']), "{}: {}".format(quiz['cid'], quiz['qname']))\
   for quiz in quizes]

  if form.validate_on_submit():
    # print(Quiz.generate_mark_list(1))
    quiz_id = form.quiz_id.data
    problems = Quiz.get_problems(quiz_id)
    print(Quiz.get_problems(quiz_id))
    return render_template('problemsList.html', title='Problems of Quiz' + quiz_id,
     quiz_id = quiz_id, problems = problems)

  return render_template('getProblems.html', title =  'Get Problems', form = form)

@app.route('/enterquiz', methods=['GET', 'POST'])
@login_required
def enterquiz():

  quizes = Quiz.get_all_quiz()
  student_quizzes = []
  for quiz in quizes:
    if Quiz.is_student_in_quiz(current_user.user_id, quiz[0]):
      student_quizzes.append(quiz)

  form = GetProblems()
  form.quiz_id.choices = [(str(quiz[0]), quiz[3]) for quiz in student_quizzes]

  if form.validate_on_submit():
    return redirect (url_for('quizformget', quiz_id=form.quiz_id.data))

  return render_template('getProblems.html', title =  'Enter Quiz', form = form)

@app.route('/quiz/<quiz_id>', methods=['GET'])
@login_required
def quizformget(quiz_id):

  student_id = current_user.user_id
  if not Quiz.is_student_in_quiz(student_id,quiz_id):
     flash('Sorry you have not enrolled for this Quiz!!' )
     return redirect (url_for('enterquiz'))

  if not Quiz.quiz_status(quiz_id)[0]:
    flash(Quiz.quiz_status(quiz_id)[1])
    return redirect(url_for('enterquiz'))

  if Quiz.quiz_attempted(quiz_id, student_id):
      flash('You have already attempted the quiz')
      return redirect(url_for('index'))
  
  problems = (Quiz.get_problems(quiz_id))
  return render_template('quiz.html', title = 'Quiz' + quiz_id, problems = problems,
   quiz_id = quiz_id)

@app.route('/quiz/<quiz_id>', methods=['POST'])
@login_required
def quizformpost(quiz_id): 

  if not Quiz.quiz_status(quiz_id)[0]:
    flash(Quiz.quiz_status(quiz_id)[1])
    return redirect(url_for('index'))

  d = request.form.to_dict()
  response_list  = [(int(pid),d[pid]) for pid in d]

  student_id = current_user.user_id
  submission_status = Quiz.insert_response(quiz_id, student_id, response_list)

  if(submission_status == True):
    flash("Successfully submitted your responses")
    return redirect('/')
  else:
    flash("Sorry could not submit your responses")
    return redirect (url_for('quizform', quiz_id=quiz_id))

@app.route('/quiz/result', methods = ['GET', 'POST'])
@login_required
def generateresult():

  faculty_id = Faculty.get_faculty_id(current_user.email)[1]
  quizes = Quiz.get_faculty_quiz(faculty_id)
  print(quizes)

  form = GetResult()
  form.quiz_id.choices = [(str(quiz['qid']), quiz['qname']) for quiz in quizes]

  if form.validate_on_submit():
    results = Quiz.generate_mark_list(form.quiz_id.data)
    print(results)
    return render_template('results.html', title = 'Results for quiz ' + form.quiz_id.data, 
                            form = form, results = results, quiz_id = form.quiz_id.data)

  return render_template('getResult.html', title =  'Select Quiz', form = form)
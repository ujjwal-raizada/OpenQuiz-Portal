import os
from OpenQuiz.student import Student
from OpenQuiz.faculty import Faculty
from OpenQuiz.quiz import Quiz
from OpenQuiz.course import Course
from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationFormStudent, RegistrationFormFaculty
from app.forms import CourseForm, StudentCourseForm, FacultyCourseForm,GetProblems
from app.forms import CreateProblem, CreateQuiz,QuizForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
  print(os.getcwd())
  username = current_user.username
  user_type = 'faculty'
  if(Faculty.get_faculty_id(username)[0] == False):
    user_type = 'student'
  return render_template('index.html', title='Home', user_type = user_type)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username = form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
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
    print(Student.create_student(form.studentid.data, form.name.data))
    user = User(username = form.username.data, email = form.email.data)
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
    user = User(username = form.username.data, email = form.email.data)
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
  if form.validate_on_submit():
    Course.create_course(form.course_id.data, form.course_name.data, int(form.ic_id.data)) 
    flash('The course has been added successfully')
    return redirect(url_for('index'))
  return render_template('courseForm.html', title = 'Add Course', form = form)

@app.route('/studentcourse', methods=['GET', 'POST'])
@login_required
def studentcourse():
  form = StudentCourseForm()
  if form.validate_on_submit():
    Course.insert_student_in_course(form.student_id.data, form.course.data)
    flash('The student has been successfully enrolled in the course')
    return redirect(url_for('index'))
  return render_template('studentCourse.html', title = 'Enroll Course', form = form)

@app.route('/facultycourse', methods=['GET', 'POST'])
@login_required
def facultycourse():
  form = FacultyCourseForm()
  if form.validate_on_submit():
    print(current_user.email)
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
  form = CreateQuiz()
  if form.validate_on_submit():    
    faculty_id = Faculty.get_faculty_id(current_user.email)
    #course = Course.get_all_course()[0][0]
    if(faculty_id[0] == False):
      flash(form.faculty_email.data + ' is not a valid faculty email')
    elif (False):#validate course name
      flash('__ is not a valid course name')
    else:
      print(Quiz.create_quiz(faculty_id[1], 'CS F211', form.quiz_name.data, form.start_time.data, form.end_time.data))
      flash('quiz created successfully')
      return redirect(url_for('index'))
  return render_template('createQuiz.html', title = 'Create Quiz', form = form)

@app.route('/createproblem', methods=['GET', 'POST'])
@login_required
def createproblem():
  user = current_user.username
  form = CreateProblem()
  if form.validate_on_submit():
    Quiz.create_problem(form.quiz_id.data,form.statement.data, form.op_1.data, form.op_2.data, form.op_3.data, form.op_4.data, form.ans.data, form.positive.data, form.negative.data)
    flash('problem created successfully')
    return redirect(url_for('index'))
  return render_template('createProblem.html', title = 'Create Problem', form = form)

@app.route('/getproblems', methods=['GET', 'POST'])
@login_required
def getproblems():
  form = GetProblems()
  if form.validate_on_submit():
    if True:#check if quiz id is valid
      problems = Quiz.get_problems(form.quiz_id.data)
      return render_template('problemsList.html', title='Hme', quiz_id = form.quiz_id.data, problems = problems)
    else:
      flash('Invalid Quiz id')
  return render_template('getProblems.html', title =  'Get Problems', form = form)

@app.route('/enterquiz', methods=['GET', 'POST'])
@login_required
def enterquiz():
  form = GetProblems()
  if form.validate_on_submit():
    if True:#check if quiz id is valid
      return redirect (url_for('quizform', quiz_id=form.quiz_id.data))
    else:
      flash('Invalid Quiz id')
  return render_template('getProblems.html', title =  'Get Problems', form = form)

@app.route('/quiz/<quiz_id>', methods=['GET', 'POST'])
@login_required
def quizform(quiz_id):
  problems = Quiz.get_problems(quiz_id);
  form = QuizForm()
  #if form.validate_on_submit():
    #print(form)
  return render_template('quiz.html', title =  'Quiz', form = form, problems=problems)
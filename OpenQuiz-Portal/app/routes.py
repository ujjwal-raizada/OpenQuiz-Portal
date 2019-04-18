import os
from OpenQuiz.student import Student
from OpenQuiz.faculty import Faculty
from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import LoginForm, RegistrationFormStudent, RegistrationFormFaculty
from app.forms import CourseForm, StudentCourseForm, FacultyCourseForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
  print(os.getcwd())
  return render_template('index.html', title='Home')

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
    user = User(username = form.username.data, email = form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    print(Student.create_student(str(form.student_id.data), str(form.name.data)))
    flash('Congratulations, you are now a registered student!')
    return redirect(url_for('login'))
  return render_template('registerStudent.html', title = 'Register Student', form = form)

@app.route('/register/faculty', methods=['GET', 'POST'])
def registerFaculty():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationFormFaculty()
  if form.validate_on_submit():
    user = User(username = form.username.data, email = form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered faculty!')
    return redirect(url_for('login'))
  return render_template('registerFaculty.html', title = 'Register Faculty', form = form)

@app.route('/addcourse', methods=['GET', 'POST'])
@login_required
def addCourse():
  form = CourseForm()
  return render_template('courseForm.html', title = 'Add Course', form = form)

@app.route('/studentcourse', methods=['GET', 'POST'])
@login_required
def studentCourse():
  form = StudentCourseForm()
  return render_template('studentCourse.html', title = 'Enroll Course', form = form)

@app.route('/facultycourse', methods=['GET', 'POST'])
@login_required
def facultyCourse():
  form = FacultyCourseForm()
  return render_template('facultyCourse.html', title = 'Enroll Course', form = form)
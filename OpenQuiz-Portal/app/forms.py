from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from OpenQuiz.student import Student
from OpenQuiz.faculty import Faculty
from OpenQuiz.course import Course

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class RegistrationFormStudent(FlaskForm):
  branch = [('B.E. –Chemical Engineering', 'B.E. –Chemical Engineering'), 
            ('B.E. –Civil', 'B.E. –Civil'), 
            ('B.E. –Computer Science', 'B.E. –Computer Science'), 
            ('B.E. –Electrical & Electronics', 'B.E. –Electrical & Electronics'), 
            ('B.E. –Electronics & Communication', 'B.E. –Electronics & Communication'),
            ('B.E. –Electronics & Instrumentation', 'B.E. –Electronics & Instrumentation'),
            ('B.E. –Mechanical', 'B.E. –Mechanical'),
            ('B. Pharm.', 'B. Pharm.'),
            ('M.Sc. –Biological Sciences', 'M.Sc. –Biological Sciences'),
            ('M.Sc. –Chemistry', 'M.Sc. –Chemistry'),
            ('M.Sc. –Economics', 'M.Sc. –Economics'),
            ('M.Sc. –Mathematics', 'M.Sc. –Mathematics'),
            ('M.Sc. –Physics', 'M.Sc. –Physics')]
  username = StringField('Username', validators = [DataRequired()])
  name = StringField('Full Name', validators = [DataRequired()])
  email = StringField('Email', validators = [DataRequired(), Email()])
  password = PasswordField('Password', validators = [DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators = [DataRequired(), EqualTo('password')])
  studentid = StringField('College ID', validators = [DataRequired()])
  studentbranch = SelectField('Branch', choices = branch, validators = [DataRequired()])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username = username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username')

  def validate_email(self, email):
    user = User.query.filter_by(email = email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address')

  def validate_studentid(self, studentid):
    temp = Student.is_student(studentid.data)
    if(temp):
      raise ValidationError('Entered ID is already registered')

class RegistrationFormFaculty(FlaskForm):
  department = [('Dept. of Chemical Engineering', 'Dept. of Chemical Engineering'),
                ('Dept. of Civil Engineering', 'Dept. of Civil Engineering'),
                ('Dept. of Computer Science', 'Dept. of Computer Science'),
                ('Dept. of Electrical and Eletronics', 'Dept. of Electrical and Eletronics'),
                ('Dept. of Mechanical Engineering', 'Dept. of Mechanical Engineering'),
                ('Dept. of Pharmacy', 'Dept. of Pharmacy'),
                ('Dept. of Biological Sciences', 'Dept. of Biological Sciences'),
                ('Dept. of Chemistry', 'Dept. of Chemistry'),
                ('Dept. of Economics', 'Dept. of Economics'),
                ('Dept. of Physics', 'Dept. of Physics'),
                ('Dept. of Mathematics', 'Dept. of Mathematics')]
  username = StringField('Username', validators = [DataRequired()])
  name = StringField('Full Name', validators = [DataRequired()])
  email = StringField('Email', validators = [DataRequired(), Email()])
  password = PasswordField('Password', validators = [DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators = [DataRequired(), EqualTo('password')])
  department = SelectField('Department', choices = department, validators = [DataRequired()])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username = username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username')

  def validate_email(self, email):
    user = User.query.filter_by(email = email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address')
    id = Faculty.get_faculty_id(email.data)
    if(id[0]):
      temp = Faculty.is_faculty(id[1])
      if(temp):
        raise ValidationError('Entered email is already registered')


class CourseForm(FlaskForm):
  faculty_list = [(str(i[0]), i[1]) for i in Faculty.get_all_faculty()]
  course_id = StringField('Enter Course ID', validators = [DataRequired()])
  course_name = StringField('Enter Course Name', validators = [DataRequired()])
  ic_id = SelectField('Select IC', choices = faculty_list, validators = [DataRequired()])
  submit = SubmitField('Add Course')

  def validate_course_id(self, course_id):
    temp = Course.is_course(course_id.data)
    if(temp):
      raise ValidationError('Entered Course is already registered')

class StudentCourseForm(FlaskForm):
  course_list = [(i[0], i[1]) for i in Course.get_all_course()]
  student_id = StringField('Enter Student ID', validators = [DataRequired()])
  course = SelectField('Select Course', choices = course_list, validators = [DataRequired()])
  submit = SubmitField('Enroll')

  def validate_student_id(self, student_id):
    temp = Student.is_student(student_id.data)
    if(not temp):
      raise ValidationError('The entered ID is not registered')

class FacultyCourseForm(FlaskForm):
  course_list = [(i[0], i[1]) for i in Course.get_all_course()]
  faculty_email = StringField('Enter Faculty Email', validators = [DataRequired()])
  course = SelectField('Select Course', choices = course_list, validators = [DataRequired()])
  submit = SubmitField('Enroll')

  def validate_faculty_email(self, faculty_email):
    temp = Faculty.is_faculty(Faculty.get_faculty_id(faculty_email.data)[0])
    if(not temp):
      raise ValidationError('The entered email is not registered')
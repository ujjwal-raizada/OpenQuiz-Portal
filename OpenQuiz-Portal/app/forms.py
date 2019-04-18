from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class RegistrationFormStudent(FlaskForm):
  username = StringField('Username', validators = [DataRequired()])
  name = StringField('Full Name', validators = [DataRequired()])
  email = StringField('Email', validators = [DataRequired(), Email()])
  password = PasswordField('Password', validators = [DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators = [DataRequired(), EqualTo('password')])
  student_id = StringField('College ID', validators = [DataRequired()])
  student_branch = StringField('Branch', validators = [DataRequired()])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username = username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username')

  def validate_email(self, email):
    user = User.query.filter_by(email = email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address')

class RegistrationFormFaculty(FlaskForm):
  username = StringField('Username', validators = [DataRequired()])
  name = StringField('Full Name', validators = [DataRequired()])
  email = StringField('Email', validators = [DataRequired(), Email()])
  password = PasswordField('Password', validators = [DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators = [DataRequired(), EqualTo('password')])
  department = StringField('Department', validators = [DataRequired()])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username = username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username')

  def validate_email(self, email):
    user = User.query.filter_by(email = email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address')

class CourseForm(FlaskForm):
  course_id = StringField('Enter Course ID', validators = [DataRequired()])
  course_name = StringField('Enter Course Name', validators = [DataRequired()])
  ic_id = StringField('Enter IC', validators = [DataRequired()])
  submit = SubmitField('Add Course')

class StudentCourseForm(FlaskForm):
  student_id = StringField('Enter Student ID', validators = [DataRequired()])
  course = StringField('Enter Course', validators = [DataRequired()])
  submit = SubmitField('Enroll')

class FacultyCourseForm(FlaskForm):
  faculty_email = StringField('Enter Faculty Email', validators = [DataRequired()])
  course = StringField('Enter Course', validators = [DataRequired()])
  submit = SubmitField('Enroll')
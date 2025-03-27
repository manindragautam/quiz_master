from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, TextAreaField, SelectField, IntegerField, DateTimeLocalField
from wtforms.validators import Email, Length, EqualTo, DataRequired

class RegisterForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    fullname = StringField('Full Name')
    qualification = StringField('Qualification')
    dob = DateField('Date of Birth', format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Submit')

class SubjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class ChapterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Submit')

class QuizForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_of_quiz = DateTimeLocalField('Date of Quiz', validators=[DataRequired()])
    time_duration = IntegerField('Time Duration (In seconds)')
    submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
    question_statement = TextAreaField('Question Statement', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    correct_option = IntegerField('Correct Option (1-4)', validators=[DataRequired()])
    submit = SubmitField('Save')
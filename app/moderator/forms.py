# app/moderator/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, HiddenField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Member, Message, Student, Course, Teacher

class MemberForm(FlaskForm):
    """
    Form for moderator to add or edit an Employee
    """
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    userName = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    emailId = StringField('Email Id', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    ROLE_CHOICES = [('','--Select--'),('parent', 'Parent'),('student','Student')]
    role = SelectField('Role', choices=ROLE_CHOICES, validators=[DataRequired()])
    grade = HiddenField('Grade')
    courseid = HiddenField('Course')
    address = StringField('Address', validators=[DataRequired()])
    school = StringField('School', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    """
    Form for student to ask a query
    """

    toperson = StringField('Sentto', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ReplyForm(FlaskForm):
    """
    Form for teacher to send reply
    """

    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Send')


class MemberEditInputForm(FlaskForm):
    """
    Form for moderator to add or edit an Employee
    """
    userName = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MemberEditForm(FlaskForm):
    """
    Form for moderator to add or edit an Employee
    """
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    emailId = StringField('Email Id', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MemberDeleteForm(FlaskForm):
    """
    Form for moderator to add or edit an Employee
    """
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    emailId = StringField('Email Id', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Delete')

class StudentForm(FlaskForm):
    """
    Form for moderator to add or edit an Employee
    """
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    userName = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    emailId = StringField('Email Id', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    #ROLE_CHOICES = [('','--Select--'),('parent', 'Parent'),('student','Student')]
    #role = SelectField('Role', choices=ROLE_CHOICES, validators=[DataRequired()])
    grade = StringField('Grade', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    #school = StringField('School', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TeacherForm(FlaskForm):
    """
    Form for moderator to add or edit an Employee
    """
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    userName = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    emailId = StringField('Email Id', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    #ROLE_CHOICES = [('','--Select--'),('parent', 'Parent'),('student','Student')]
    #role = SelectField('Role', choices=ROLE_CHOICES, validators=[DataRequired()])
    #course = SelectField('Course', validators=[DataRequired()])
    course = QuerySelectField(query_factory=lambda: Course.query.all(),
                                  get_label="id")
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostBroadcastForm1(FlaskForm):
    """
    Form for moderator and admin to post a broadcast
    """
    tag = SelectField('Broadcast to', choices=[('all', 'all'), ('school', 'school')],
                      validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

class StaffForm(FlaskForm):
    """
    Form for moderator to add or edit an Employee
    """
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    userName = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    emailId = StringField('Email Id', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    #ROLE_CHOICES = [('','--Select--'),('parent', 'Parent'),('student','Student')]
    #role = SelectField('Role', choices=ROLE_CHOICES, validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    #school = StringField('School', validators=[DataRequired()])
    submit = SubmitField('Submit')

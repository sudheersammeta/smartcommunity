# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, ValidationError, HiddenField
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Employee, Student, Member, School
from sqlalchemy.orm import load_only

class RegistrationForm(FlaskForm) :
       #def get_schoolname()   :
         #return School.query.with_entities(School.schoolname)
         #return School.schoolname
         #return School.schoolname.query
       emailid = StringField('Email', validators=[DataRequired(), Email()])
       username = StringField('Username', validators=[DataRequired()])
       firstname = StringField('First Name', validators=[DataRequired()])
       lastname = StringField('Last Name', validators=[DataRequired()])
       role = HiddenField('Role Name', default="parent")
       password = PasswordField('Password', validators=[
                                        DataRequired(),EqualTo('password')
                                        ])
       #schoolname = QuerySelectField('School Name',query_factory=lambda: School.query.with_entities(School.schoolname) ,allow_blank=True)
       #schoolname = StringField('School Name', validators=[DataRequired()])
       #schoolname = QuerySelectField(query_factory=lambda: School.query.all(),
                                  #get_label="schoolname")
       schoolname = QuerySelectField(query_factory=lambda: School.query.all(),
                                  get_label="schoolname")
       address = StringField('Address', validators=[DataRequired()])        
       
       confirmpassword = PasswordField('Confirm Password')
       phone = StringField('phone', validators=[DataRequired()])
    
       submit = SubmitField('Register')
       #def get_schoolname()   :
         #return School.query.with_entities(School.schoolname)

    #def validate_email(self, field):
        #if Employee.query.filter_by(email=field.data).first():
            #raise ValidationError('Email is already in use.')

    #def validate_username(self, field):
        #if Employee.query.filter_by(username=field.data).first():
            #raise ValidationError('Username is already in use.')
class ModeratorRegistrationForm(FlaskForm) :
    emailid = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    role = HiddenField('Role Name', default="moderator")
    password = PasswordField('Password', validators=[
                                        DataRequired()])
                                        
    #school_name = StingField('School Name', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[
                                        DataRequired(),
                                        EqualTo('password')
                                        ])
    phone = StringField('phone', validators=[DataRequired()])
    address = StringField('School City', validators=[DataRequired()])
    schoolname = StringField('School Name', validators=[DataRequired()])
    #schooladdress = StringField('schooladress', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')
      

class MemberRegistrationForm(FlaskForm):
    """
    Form for members to create new account
    """
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    role = SelectField('Role Name', choices=[('parent', 'parent'), ('moderator', 'moderator')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    emailid = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Member.query.filter_by(emailid=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Member.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

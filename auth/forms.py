# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, ValidationError, HiddenField
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import School
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

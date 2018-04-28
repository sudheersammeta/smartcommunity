# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_login import current_user, login_required

from ..models import Department, Role, School, Member, Grade, Course, Parent

class ReplyForm(FlaskForm):
    """
    Form for teacher to send reply
    """

    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Send')


class QueryForm(FlaskForm):
    """
    Form for student to ask a query
   
    tag = SelectField('tag', choices=[('subject', 'subject'), ('fees', 'fees'), ('holidays', 'holidays'), ('other', 'other')],
                       validators=[DataRequired()])
    studentemailid = StringField('StudentEmailID', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
"""
    tag = SelectField('tag', choices=[('subject', 'subject'), ('fees', 'fees'), ('holidays', 'holidays'), ('other', 'other')],
                       validators=[DataRequired()])
    #studentid = StringField('Student ID', validators=[DataRequired()])
    """
    , Member.query.filter_by(username=form.username.data).first())
    """
    #studentid = QuerySelectField(query_factory=lambda: Parent.query.filter_by(parentid=current_user.id).first(),get_label="studentid")
    studentid = QuerySelectField(query_factory=lambda: Parent.query.filter_by(parentid=current_user.id),
                                  get_label="studentid")
    
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
class MessageForm(FlaskForm):
    """
    Form for student to ask a query
    """

    toperson = StringField('Sentto', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class StudentAddForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    studentid = StringField('Student ID', validators=[DataRequired()])
    #schoolname = StringField('School Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SchoolForm(FlaskForm):
    """
    Form for admin to add or edit a school
    """
    schoolname = StringField('School Name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

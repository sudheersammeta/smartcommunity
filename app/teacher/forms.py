# app/teacher/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, Member, Message

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ForwardQueryForm(FlaskForm):
    """
    Form for teachr to submit leave application
    """
    status = RadioField('Status', choices=[('active','Active'), ('notactive','NotActive')])
    substitute = StringField('Subtitute Person')
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class MessageForm(FlaskForm):
    """
    Form for student to ask a query
    """

    toperson = StringField('Send to', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ReplyForm(FlaskForm):
    """
    Form for teacher to send reply
    """

    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Send')


class EmployeeAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

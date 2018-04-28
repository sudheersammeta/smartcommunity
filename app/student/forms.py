# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Department, Role, School, Member, Grade, Course, Mappingquery, Message, Query, Student

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

class ReplyForm(FlaskForm):
    """
    Form for teacher to send reply
    """

    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Send')


class QueryForm(FlaskForm):
    """
    Form for student to ask a query
    """
    tag = SelectField('tag', choices=[('subject', 'subject'), ('fees', 'fees'), ('holidays', 'holidays'), ('other', 'other')],
                       validators=[DataRequired()])
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

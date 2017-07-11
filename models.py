# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class School(db.Model):
    """
    Create a School table
    """

    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    schoolname = db.Column(db.String(100), unique=True)
    city = db.Column(db.String(15))
    members = db.relationship('Member', backref='schooldetails', lazy='dynamic')

    def __repr__(self):
        return '<School: {}>'.format(self.schoolname)

class Member(UserMixin, db.Model):
    """
    Create a Member table
    """
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    emailid = db.Column(db.String(30))
    phone = db.Column(db.String(10))
    role = db.Column(db.String(10))
    address = db.Column(db.String(100))
    lastlogin = db.Column(db.DateTime)
    schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))
    teachers = db.relationship('Teacher', backref='teacher',
                                lazy='dynamic')
    parents = db.relationship('Parent', backref='details', primaryjoin='Member.id==Parent.parentid', lazy='dynamic')
    staffs = db.relationship('Staff', backref='staff', lazy='dynamic')
    students = db.relationship('Student', backref='student', lazy='dynamic')
    queries = db.relationship('Query', backref='querydetails', primaryjoin='Member.id==Query.senderid', lazy='dynamic')
    forwards = db.relationship('Forward', backref='forwarddetails', primaryjoin='Member.id==Forward.originalid', lazy='dynamic')
    messages = db.relationship('Message', backref='messagedetails', primaryjoin='Member.id==Message.senderid', lazy='dynamic')

    def __repr__(self):
        return '<Member: {}>'.format(self.emailid)

class Parent(UserMixin, db.Model):
    """
    Create parents table
    """
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True)
    parentid = db.Column(db.Integer, db.ForeignKey('members.id'))
    studentid = db.Column(db.Integer, db.ForeignKey('members.id'))
    schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))

    def __repr__(self):
        return '<Parent: {}>'.format(self.parentid)
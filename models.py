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

class Grade(db.Model):
      """
      Create grades table
      """
      __tablename__ = 'grades'

      id = db.Column(db.Integer, primary_key=True)
      grade = db.Column(db.Integer)
      courseid = db.Column(db.Integer, db.ForeignKey('courses.id'))
      schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))

      def __repr__(self):
         return '<Grade: {}>'.format(self.grade)

class Query(db.Model):
      """
      Create queries table
      """
      __tablename__ = 'queries'

      id = db.Column(db.Integer, primary_key=True)
      senderid = db.Column(db.Integer, db.ForeignKey('members.id'))
      receiverid = db.Column(db.Integer, db.ForeignKey('members.id'))
      tag = db.Column(db.String(10))
      description = db.Column(db.String(500))
      reply = db.Column(db.String(500))
      creationtime = db.Column(db.DateTime)
      schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))

      def __repr__(self):
         return '<Query: {}>'.format(self.tag)

class Message(db.Model):
      """
      Create messages table
      """
      __tablename__ = 'messages'

      id = db.Column(db.Integer, primary_key=True)
      senderid = db.Column(db.Integer, db.ForeignKey('members.id'))
      receiverid = db.Column(db.Integer, db.ForeignKey('members.id'))
      title = db.column(db.String(50))
      description = db.Column(db.String(500))
      reply = db.Column(db.String(500))
      isread = db.Column(db.Boolean)

      def __repr__(self):
         return '<Message: {}>'.format(self.isread)

class Broadcast(db.Model):
      """
      Create broadcasts table
      """
      __tablename__ = 'broadcasts'

      id = db.Column(db.Integer, primary_key=True)
      broadcastall = db.Column(db.Boolean)
      description = db.Column(db.String(500))
      creationtime = db.Column(db.DateTime)
      schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))

      def __repr__(self):
         return '<Broadcast: {}>'.format(self.creationtime)

class Forward(db.Model):
      """
      Create forwards table
      """
      __tablename__ = 'forwards'

      id = db.Column(db.Integer, primary_key=True)
      originalid= db.Column(db.Integer, db.ForeignKey('members.id'))
      replacerid= db.Column(db.Integer, db.ForeignKey('members.id'))
      expirytime = db.Column(db.DateTime)

      def __repr__(self):
         return '<Forward: {}>'.format(self.replacerid)

class Mappingquery(db.Model):
      """
      Create mappingquery table
      """
      __tablename__ = 'mappings'

      id = db.Column(db.Integer, primary_key=True)
      tag= db.Column(db.String(10))
      memberid= db.Column(db.Integer, db.ForeignKey('members.id'))

      def __repr__(self):
         return '<Mappingquery: {}>'.format(self.memberid)

class Student(UserMixin, db.Model):
        """
        Create students table
        """
        __tablename__ = 'students'

        id = db.Column(db.Integer, primary_key=True)
        studentid = db.Column(db.Integer, db.ForeignKey('members.id'))
        grade = db.Column(db.Integer, db.ForeignKey('grades.grade'))
        section = db.Column(db.Integer)
        schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))

        def __repr__(self):
            return '<Student: {}>'.format(self.studentid)

class Course(db.Model):
      """
      Create courses table
      """
      __tablename__ = 'courses'

      id = db.Column(db.Integer, primary_key=True)
      coursename = db.Column(db.String(10))
      schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))

      def __repr__(self):
          return '<Course: {}>'.format(self.coursename)

class Teacher(UserMixin, db.Model):
        """
        Create teachers table
        """
        __tablename__ = 'teachers'

        id = db.Column(db.Integer, primary_key=True)
        teacherid = db.Column(db.Integer, db.ForeignKey('members.id'))
        courseid = db.Column(db.Integer, db.ForeignKey('courses.id'))
        onleave = db.Column(db.Boolean)
        schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))

        def __repr__(self):
            return '<Teacher: {}>'.format(self.teacherid)

class Staff(UserMixin, db.Model):
        """
        Create staffs table
        """
        __tablename__ = 'staffs'

        id = db.Column(db.Integer, primary_key=True)
        staffid = db.Column(db.Integer, db.ForeignKey('members.id'))
        onleave = db.Column(db.Boolean)
        schoolid = db.Column(db.Integer, db.ForeignKey('schools.id'))

        def __repr__(self):
            return '<Staff: {}>'.format(self.staffid)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

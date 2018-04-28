# app/auth/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm, ModeratorRegistrationForm
from .. import db
from ..models import Employee, Member, Student, Teacher, Parent, Grade, Course, Query, School, Staff

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an employee to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        #if School.query.filter_by(schoolname=form.schoolname.data).first() is not None:
            #school = School.query.filter_by(schoolname=form.schoolname.data).first()
            member = Member(firstname=form.firstname.data,
                                lastname=form.lastname.data,
                                username=form.username.data,
                                password=form.password.data,
                                emailid=form.emailid.data,
                                phone=form.phone.data,
                                role=form.role.data,
                                address=form.address.data,
                                schoolid=form.schoolname.data.id)
            db.session.add(member)
            db.session.commit()
            flash('You have successfully registered! You may now login.')

            # redirect to the login page
            return redirect(url_for('auth.login'))
        #else:
            #flash('Invalid school name')
            #return redirect(url_for('auth.login'))


    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/register/moderator', methods=['GET', 'POST'])
def moderatorregister() :

    form = ModeratorRegistrationForm()
    if form.validate_on_submit():

        school = School(schoolname=form.schoolname.data,
                              city=form.address.data)
        db.session.add(school)
        db.session.commit()
        school = School.query.filter_by(schoolname=form.schoolname.data).first()


        member = Member(firstname=form.firstname.data,
                            lastname=form.lastname.data,
                            username=form.username.data,
                            password=form.password.data,
                            emailid=form.emailid.data,
                            phone=form.phone.data,
                            role=form.role.data,
                            address=form.address.data,
                            schoolid=school.id)

        db.session.add(member)
        db.session.commit()
        #school = School(schoolname=form.schoolname.data,
                              #city=form.address.data)
        #db.session.add(school)
        #db.session.commit()
        #school = School.query.filter_by(schoolname=form.schoolname.data).first()
        #member = Member.query.filter_by(username=form.username.data).first()
        #member.schoolid = school.id



        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/moderatorregister.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        member = Member.query.filter_by(username=form.username.data).first()
        if member is not None:
            if (member.password == form.password.data):
                # log employee in
                login_user(member)

                # redirect to the appropriate dashboard page
                if (member.role == 'admin'):
                    return redirect(url_for('home.admin_dashboard'))
                elif (member.role == 'student'):
                    return redirect(url_for('home.student_dashboard'))
                elif (member.role == 'moderator'):
                    return redirect(url_for('home.moderator_dashboard'))
                elif (member.role == 'teacher'):
                    return redirect(url_for('home.teacher_dashboard'))
                elif (member.role == 'parent'):
                    return redirect(url_for('home.parent_dashboard'))
                elif (member.role == 'staff'):
                    return redirect(url_for('home.staff_dashboard'))
            else:
                flash('Invalid Password')

        # when login details are incorrect
        else:
            flash('Invalid Username')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

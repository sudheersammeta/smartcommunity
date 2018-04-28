# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import DepartmentForm, RoleForm, ReplyForm, EmployeeAssignForm, SchoolForm, PostBroadcastForm, MessageForm
from .. import db
from ..models import Department, Role, Employee, School, Broadcast, Message, Member

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not (current_user.role == 'admin'):
        abort(403)

# Department Views

@admin.route('/departments', methods=['GET', 'POST'])
@login_required
def list_departments():
    """
    List all departments
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departments/departments.html',
                           departments=departments, title="Departments")


@admin.route('/reply_message/<int:id>', methods=['GET', 'POST'])
@login_required
def reply_message(id):
    """
    Reply to a message
    """
    message = Message.query.get_or_404(id)
    form = ReplyForm()
    if form.validate_on_submit():
        #member = Member.query.filter_by(username=current_user.username)
        sender = Member.query.filter_by(id=current_user.id).first()
        receiver = Member.query.filter_by(id=message.senderid).first()
        reply = Message(senderid=sender.id, description=form.description.data, receiverid=receiver.id, isread=False)
        #grade = Grade.query.filter_by(id=student.grade)

        # add message to the database
        db.session.add(reply)
        db.session.commit()
        flash('You have successfully replied to the message.')

        return redirect(url_for('home.admin_dashboard'))
    return render_template('admin/messages/reply_message.html', form=form, title='reply')


@admin.route('/schools', methods=['GET', 'POST'])
@login_required
def list_schools():
    """
    List all schools
    """
    check_admin()

    schools = School.query.all()

    return render_template('admin/schools/schools.html',
                           schools=schools, title="Schools")

@admin.route('/messages', methods=['GET', 'POST'])
@login_required
def post_message():
    """
    writing a message
    """

    form = MessageForm()

    if form.validate_on_submit():
        #member = Member.query.filter_by(username=current_user.username)
        sender = Member.query.filter_by(id=current_user.id).first()
        receiver = Member.query.filter_by(username=form.toperson.data).first()
        message = Message(senderid=sender.id, description=form.description.data, receiverid=receiver.id, isread=False)
        #grade = Grade.query.filter_by(id=student.grade)

        # add message to the database
        db.session.add(message)
        db.session.commit()
        flash('You have successfully submitted message.')

        return redirect(url_for('home.admin_dashboard'))
    return render_template('admin/messages/message_post.html', form=form, title='Messages')


@admin.route('/schools/add', methods=['GET', 'POST'])
@login_required
def add_school():
    """
    Add a school to the database
    """
    check_admin()

    add_school = True

    form = SchoolForm()
    if form.validate_on_submit():
        school = School(schoolname=form.schoolname.data,
                                city=form.city.data)
        try:
            # add school to the database
            db.session.add(school)
            db.session.commit()
            flash('You have successfully added a new school.')
        except:
            # in case department name already exists
            flash('Error: school name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_schools'))

    # load department template
    return render_template('admin/schools/school.html', action="Add",
                           add_school=add_school, form=form,
                           title="Add School")

@admin.route('/schools/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_school(id):
    """
    Edit a school
    """
    check_admin()

    add_school = False

    school = School.query.get_or_404(id)
    form = SchoolForm(obj=school)
    if form.validate_on_submit():
        school.schoolname = form.schoolname.data
        school.city = form.city.data
        db.session.commit()
        flash('You have successfully edited the school.')

        # redirect to the schools page
        return redirect(url_for('admin.list_schools'))

    form.city.data = school.city
    form.schoolname.data = school.schoolname
    return render_template('admin/schools/school.html', action="Edit",
                           add_school=add_school, form=form,
                           school=school, title="Edit School")

@admin.route('/schools/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_school(id):
    """
    Delete a school from the database
    """
    check_admin()

    school = School.query.get_or_404(id)
    db.session.delete(school)
    db.session.commit()
    flash('You have successfully deleted the school.')

    # redirect to the departments page
    return redirect(url_for('admin.list_schools'))

    return render_template(title="Delete School")



@admin.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    """
    Add a department to the database
    """
    check_admin()

    add_department = True

    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data,
                                description=form.description.data)
        try:
            # add department to the database
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_departments'))

    # load department template
    return render_template('admin/departments/department.html', action="Add",
                           add_department=add_department, form=form,
                           title="Add Department")

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    """
    Edit a department
    """
    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.')

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action="Edit",
                           add_department=add_department, form=form,
                           department=department, title="Edit Department")

@admin.route('/departments/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    """
    Delete a department from the database
    """
    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the departments page
    return redirect(url_for('admin.list_departments'))

    return render_template(title="Delete Department")


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

@admin.route('/employees')
@login_required
def list_employees():
    """
    List all employees
    """
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')

@admin.route('/employees/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_employee(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    employee = Employee.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if employee.is_admin:
        abort(403)

    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')

@admin.route('/broadcasts', methods=['GET', 'POST'])
@login_required
def post_broadcast():
    """
    posting broadcast for all community
    """

    check_admin()
    form = PostBroadcastForm()

    if form.validate_on_submit():
        message = Broadcast(broadcastall=True, description=form.message.data)

        # add broadcast message to the database
        db.session.add(message)
        db.session.commit()
        flash('You have successfully posted a message in community.')

        return redirect(url_for('home.admin_dashboard'))
    return render_template('admin/broadcasts/admin_broadcast.html', form=form, title='Broadcasts')

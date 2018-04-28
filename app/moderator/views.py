# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import moderator
from .forms import MemberForm, MemberEditInputForm, ReplyForm, MemberEditForm, MemberDeleteForm, TeacherForm, StudentForm, StaffForm, MessageForm, PostBroadcastForm1
from .. import db
from ..models import Member, School, Course, Teacher, Student, Staff

def check_moderator():
    """
    Prevent non-moderators from accessing the page
    """
    if not current_user.role == 'moderator':
        abort(403)

@moderator.route('/broadcasts', methods=['GET', 'POST'])
@login_required
def post_broadcast():
    """
    posting broadcast for all community
    """

    check_moderator()
    form = PostBroadcastForm1()

    if form.validate_on_submit():
        member=Member.query.filter_by(id=current_user.id).first()
        if (form.tag.data == 'all'):
            message = Broadcast(broadcastall=True, description=form.message.data, schoolid=member.schoolid)

        else:
            message = Broadcast(broadcastall=False, description=form.message.data, schoolid=member.schoolid)

        # add broadcast message to the database
        db.session.add(message)
        db.session.commit()
        flash('You have successfully posted a message in community.')

        return redirect(url_for('home.moderator_dashboard'))
    return render_template('moderator/broadcasts/moderator_broadcast.html', form=form, title='Broadcasts')


#member asking MesageForm
@moderator.route('/messages', methods=['GET', 'POST'])
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

        return redirect(url_for('home.moderator_dashboard'))
    return render_template('moderator/messages/message_post.html', form=form, title='Messages')


@moderator.route('/reply_message/<int:id>', methods=['GET', 'POST'])
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

        return redirect(url_for('home.moderator_dashboard'))
    return render_template('moderator/messages/reply_message.html', form=form, title='reply')


@moderator.route('/members/add', methods=['GET', 'POST'])
@login_required
def add_member():
    """
    Add a member to a School
    """
    check_moderator()

    add_member = True

    form = MemberForm()
    if form.validate_on_submit():
        member = Member(firstname=form.firstName.data,
                            lastname=form.lastName.data,
                            username=form.userName.data,
                            password=form.password.data,
                            emailid=form.emailId.data,
                            phone=form.phone.data,
                            role=form.role.data,
                            address=form.address.data,
                            schoolid=current_user.schoolid)
        try:
            # add department to the database
            db.session.add(member)
            db.session.commit()
            flash('You have successfully added a new Member.')
        except:
            # in case department name already exists
            flash('Error: Member name already exists.')

        # redirect to departments page
        return redirect(url_for('home.moderator_dashboard'))

    # load department template
    return render_template('moderator/members/member.html', action="Add",
                           add_member=add_member, form=form,
                           title="Add Member")

@moderator.route('/members/edit', methods=['GET', 'POST'])
@login_required
def edit_member_input():
    """
    Input details of member to be edited
    """
    check_moderator()
    add_member = False

    form = MemberEditInputForm()
    if form.validate_on_submit():
        member=Member.query.filter_by(username=form.userName.data).first()
        if member is None:
            flash('Invalid username')
        else:
            return redirect(url_for('moderator.edit_member', username=form.userName.data))

    return render_template('moderator/members/editMember.html', form=form, title='Edit Member')

@moderator.route('/members/delete', methods=['GET', 'POST'])
@login_required
def delete_member_input():
    """
    Input details of member to be edited
    """
    check_moderator()
    add_member = False

    form = MemberEditInputForm()
    if form.validate_on_submit():
        member=Member.query.filter_by(username=form.userName.data).first()
        if member is None:
            flash('Invalid username')
        else:
            return redirect(url_for('moderator.delete_member', username=form.userName.data))

    return render_template('moderator/members/editMember.html', form=form, title='Delete Member')


@moderator.route('/members/delete/<username>', methods=['GET', 'POST'])
@login_required
def delete_member(username):
    """
    Edit a member
    """
    check_moderator()

    add_member = False

    member=Member.query.filter_by(username=username).first()

    if not (member.schoolid == current_user.schoolid):
        #abort(403)
        flash('You have no permissions to delete members of other school.')
        # redirect to the moderator dashboard page
        return redirect(url_for('moderator.delete_member_input'))

    form = MemberDeleteForm(obj=member)
    if form.validate_on_submit():
        member.firstname=form.firstName.data
        member.lastname=form.lastName.data
        #member.username=form.userName.data
        #password=form.password.data,
        member.emailid=form.emailId.data
        member.phone=form.phone.data
        member.role=form.role.data
        member.address=form.address.data
        print(member.id)
        #db.session.delete(member.id)
        print('success')
        db.session.query(Member).filter_by(username=username).delete()
        db.session.commit()
        flash('Member deleted successfully.')

        # redirect to the schools page
        return redirect(url_for('home.moderator_dashboard'))

    form.firstName.data = member.firstname
    form.lastName.data = member.lastname
    #form.userName.data = member.username
    form.emailId.data = member.emailid
    form.phone.data = member.phone
    form.role.data = member.role
    form.address.data = member.address
    return render_template('moderator/members/member.html', action="Delete",
                           add_member=add_member, form=form,
                           title="Delete Member")


@moderator.route('/members/edit/<username>', methods=['GET', 'POST'])
@login_required
def edit_member(username):
    """
    Edit a member
    """
    check_moderator()

    add_member = False

    member=Member.query.filter_by(username=username).first()

    if not (member.schoolid == current_user.schoolid):
        #abort(403)
        flash('You have no permissions to edit members of other school.')
        # redirect to the moderator dashboard page
        return redirect(url_for('home.moderator_dashboard'))

    form = MemberEditForm(obj=member)
    if form.validate_on_submit():
        member.firstname=form.firstName.data
        member.lastname=form.lastName.data
        #member.username=form.userName.data
        #password=form.password.data,
        member.emailid=form.emailId.data
        member.phone=form.phone.data
        member.role=form.role.data
        member.address=form.address.data
        #db.session.add()
        db.session.commit()
        flash('Member details updated successfully.')

        # redirect to the schools page
        return redirect(url_for('home.moderator_dashboard'))

    form.firstName.data = member.firstname
    form.lastName.data = member.lastname
    #form.userName.data = member.username
    form.emailId.data = member.emailid
    form.phone.data = member.phone
    form.role.data = member.role
    form.address.data = member.address
    return render_template('moderator/members/member.html', action="Edit",
                           add_member=add_member, form=form,
                           title="Edit Member")

@moderator.route('/staff/add', methods=['GET', 'POST'])
@login_required
def add_staff():
    """
    Add a member to a School
    """
    check_moderator()

    add_member = True

    form = StaffForm()
    if form.validate_on_submit():
        member = Member(firstname=form.firstName.data,
                            lastname=form.lastName.data,
                            username=form.userName.data,
                            password=form.password.data,
                            emailid=form.emailId.data,
                            phone=form.phone.data,
                            role='staff',
                            address=form.address.data,
                            schoolid=current_user.schoolid)
        try:
            # add department to the database
            db.session.add(member)
            member = db.session.query(Member).filter_by(username=form.userName.data).first()
            staff = Staff(staffid=member.id,
                                onleave=False,
                                schoolid=current_user.schoolid)
            db.session.add(staff)
            db.session.commit()
            flash('You have successfully added a new Staff Member.')
        except:
            # in case department name already exists
            flash('Error: Member name already exists.')

        # redirect to departments page
        return redirect(url_for('home.moderator_dashboard'))

    # load department template
    return render_template('moderator/members/member.html', action="Add",
                           add_member=add_member, form=form,
                           title="Add Staff Member")


@moderator.route('/teachers/add', methods=['GET', 'POST'])
@login_required
def add_teacher():
    """
    Add a member to a School
    """
    check_moderator()

    add_member = True

    form = TeacherForm()
    #form.course.choices = [(row.id, row.coursename) for row in Course.query.filter_by(schoolid = current_user.schoolid).all()]
    if form.validate_on_submit():
        member = Member(firstname=form.firstName.data,
                            lastname=form.lastName.data,
                            username=form.userName.data,
                            password=form.password.data,
                            emailid=form.emailId.data,
                            phone=form.phone.data,
                            role='teacher',
                            address=form.address.data,
                            schoolid=current_user.schoolid)
        #try:
        # add department to the database
        db.session.add(member)
        member = db.session.query(Member).filter_by(username=form.userName.data).first()
        teacher = Teacher(teacherid=member.id,
                            courseid = form.course.data.id,
                            onleave=False,
                            schoolid=current_user.schoolid)
        db.session.add(teacher)
        db.session.commit()
        flash('You have successfully added a new Teacher.')
    #except:
            # in case teacher already exists
            #flash('Error: Member already exists.')

        # redirect to moderator dashboard page
        return redirect(url_for('home.moderator_dashboard'))

    # load add teacher template
    return render_template('moderator/members/member.html', action="Add",
                           add_member=add_member, form=form,
                           title="Add Teacher")


@moderator.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Add a member to a School
    """
    check_moderator()

    add_member = True

    form = StudentForm()
    #form.course.choices = [(row.id, row.coursename) for row in Course.query.filter_by(schoolid = current_user.schoolid).all()]
    if form.validate_on_submit():
        member = Member(firstname=form.firstName.data,
                            lastname=form.lastName.data,
                            username=form.userName.data,
                            password=form.password.data,
                            emailid=form.emailId.data,
                            phone=form.phone.data,
                            role='student',
                            address=form.address.data,
                            schoolid=current_user.schoolid)
        #try:
        # add department to the database
        db.session.add(member)
        member = db.session.query(Member).filter_by(username=form.userName.data).first()
        student = Student(studentid=member.id,
                            grade = form.grade.data,
                            schoolid=current_user.schoolid)
        db.session.add(student)
        db.session.commit()
        flash('You have successfully added a new Student.')
    #except:
            # in case department name already exists
            #flash('Error: Member already exists.')

        # redirect to departments page
        return redirect(url_for('home.moderator_dashboard'))

    # load department template
    return render_template('moderator/members/member.html', action="Add",
                           add_member=add_member, form=form,
                           title="Add Member")


@moderator.route('/billing')
@login_required
def view_billing():

    check_moderator()

    school = School.query.get_or_404(current_user.schoolid)

    user_count = db.session.query(Member).filter_by(schoolid=school.id).count()

    bill=calculate_bill(user_count)
    #bill=100
    return render_template('moderator/billings/billing.html', action="View",
                           name=school.schoolname, user_count=user_count,
                           bill=bill,
                           title="View Billing")


def calculate_bill(user_count):

    return user_count * 0.25

@moderator.route('/charts')
@login_required
def view_charts():

    check_moderator()

    school = School.query.get_or_404(current_user.schoolid)

    user_count = db.session.query(Member).filter_by(schoolid=school.id).count()
    teacher_count = db.session.query(Member).filter_by(role='teacher', schoolid=school.id).count()
    staff_count = db.session.query(Member).filter_by(role='staff', schoolid=school.id).count()
    student_count = db.session.query(Member).filter_by(role='student', schoolid=school.id).count()
    parent_count = db.session.query(Member).filter_by(role='parent', schoolid=school.id).count()

    school_details={'teacher_count' : teacher_count, 'staff_count' : staff_count,
                    'student_count': student_count, 'parent_count': parent_count }

    #db.session.query(students.grade, func.count(students.grade)).group_by(students.grade).all()
    class_count=db.session.query(Student.grade, db.func.count(Student.grade).label("count")).filter_by(schoolid=school.id).group_by(Student.grade).all()
    #=db.session.query(Student).filter_by(schoolid=school.id).all()
    print(class_count)
    #class_count=0
    return render_template('moderator/charts/chart.html', action="View",
                           name=school.schoolname, user_count=user_count,
                           school_details=school_details, class_count=class_count, title="Charts")

######################################################################################################################################

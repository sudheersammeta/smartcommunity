# app/teacher/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .forms import DepartmentForm, RoleForm, EmployeeAssignForm, MessageForm, ReplyForm, ForwardQueryForm
from .. import db
from ..models import School, Member, Teacher, Broadcast, Query, Message, Forward

from . import teacher

def check_teacher():
    """
    Prevent non-students from accessing the page
    """
    if not current_user.role == 'teacher':
        abort(403)

#member asking MesageForm
@teacher.route('/messages', methods=['GET', 'POST'])
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

        return redirect(url_for('home.teacher_dashboard'))
    return render_template('teacher/messages/message_post.html', form=form, title='Messages')

@teacher.route('/reply_message/<int:id>', methods=['GET', 'POST'])
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

        return redirect(url_for('home.teacher_dashboard'))
    return render_template('teacher/messages/reply_message.html', form=form, title='reply')



# View queries and reply
@teacher.route('/teacher/query')
@login_required
def view_queries():
    """
     Get the queries for this teacher from query table and display
    """

    query = Query.query.filter_by(receiverid=current_user.id)
    return render_template('teacher/query.html', query=query, title="Query")

@teacher.route('/apply_leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    """
    Apply leave - teacher and name a substitute
    """

    form = ForwardQueryForm()
    if form.validate_on_submit():
        #member = Member.query.filter_by(username=current_user.username)
        if (form.status.data == 'notactive'):
            replacer = Member.query.filter_by(username=form.substitute.data).first()
            teacher = Teacher.query.filter_by(teacherid=current_user.id).update({"onleave" : True})
            forward = Forward(originalid=current_user.id, replacerid=replacer.id)
            db.session.add(forward)
            #db.session.commit()
            #flash('You have successfully applied for leave.')

        if (form.status.data == 'active'):
            teacher = Teacher.query.filter_by(teacherid=current_user.id).update({"onleave" : False})
        db.session.commit()
            #flash('Welcome back from leave.')
        return redirect(url_for('home.teacher_dashboard'))
    return render_template('teacher/applyleave.html', form=form, title="Leave Status")

'''
#View school broadcast
@teacher.route('/view_school_broadcast', methods=['GET', 'POST'])
@login_required
def view_broadcast():
    """
    View the broadcast messages for last N days ??
    """

    member = Member.query.filter_by(username=current_user.username).first()
    school = School.query.filter_by(id=member.schoolid).first()

    broadcast = Broadcast.query.filter_by(schoolid=school.id)
    return render_template('teacher/broadcast.html', schoolname=school.schoolname, broadcast=broadcast, title="School broadcast")

#View community broadcast
@teacher.route('/view_community_broadcast', methods=['GET', 'POST'])
@login_required
def view_community_broadcast():
    """
    View community broadcast messages as long as broadcastall value is 1 for that message
    """

    broadcast = Broadcast.query.filter_by(broadcastall=1)
    return render_template('teacher/community_broadcast.html', broadcast=broadcast, title="Community broadcast")


'''

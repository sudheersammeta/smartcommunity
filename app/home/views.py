# app/home/views.py

from flask import render_template
from flask_login import login_required
from flask import abort, render_template
from flask_login import current_user, login_required

from . import home
from .. import db
from ..models import School, Member, Broadcast, Message, Query

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.role == 'admin':
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

#add moderator dashboard view
@home.route('/moderator/dashboard')
@login_required
def moderator_dashboard():
    # prevent non-admins from accessing the page
    #if not (current_user.role == 'student'):
        #abort(403)
    print(current_user.role)
    return render_template('home/moderator_dashboard.html', title="Dashboard")

#add student dashboard view
@home.route('/student/dashboard')
@login_required
def student_dashboard():
    # prevent non-admins from accessing the page
    #if not (current_user.role == 'student'):
        #abort(403)
    print(current_user.role)
    return render_template('home/student_dashboard.html', title="Student Dashboard")

#add teacher dashboard view
@home.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    # prevent non-teachers from accessing the page
    #if not (current_user.role == 'teacher'):
        #abort(403)
    print(current_user.role)
    return render_template('home/teacher_dashboard.html', title="Dashboard")

@home.route('/parent/dashboard')
@login_required
def parent_dashboard():
    # prevent non-teachers from accessing the page
    #if not (current_user.role == 'teacher'):
        #abort(403)
    print(current_user.role)
    return render_template('home/parent_dashboard.html', title="Dashboard")

@home.route('/staff/dashboard')
@login_required
def staff_dashboard():
    # prevent non-teachers from accessing the page
    #if not (current_user.role == 'teacher'):
        #abort(403)
    print(current_user.role)
    return render_template('home/staff_dashboard.html', title="Staff Dashboard")

#View query replies
@home.route('/view_query_replies', methods=['GET', 'POST'])
@login_required
def view_query_replies():
    """
    Get the queries for this teacher from query table and display
    """

    query = Query.query.filter_by(senderid=current_user.id)

    return render_template('home/view_query_replies.html', query=query, title="View replies")

#Display query reply
@home.route('/view_reply/<int:id>', methods=['GET', 'POST'])
@login_required
def view_reply(id):
    """
    Get the queries for this teacher from query table and display
    """

    query = Query.query.filter_by(id=id).first()

    return render_template('home/view_reply.html', query=query, title="View reply")

    
#View school broadcast
@home.route('/view_school_broadcast', methods=['GET', 'POST'])
@login_required
def view_school_broadcast():
    """
    View the broadcast messages for last N days ??
    """

    member = Member.query.filter_by(username=current_user.username).first()
    school = School.query.filter_by(id=member.schoolid).first()

    broadcast = Broadcast.query.filter_by(schoolid=school.id)
    return render_template('home/view_school_broadcast.html', schoolname=school.schoolname, broadcast=broadcast, title="School broadcast")

@home.route('/view_messages', methods=['GET', 'POST'])
@login_required
def view_messages():
    """
    View the messages for last N days ??
    """

    member = Member.query.filter_by(id=current_user.id).first()

    receivedmsgs = Message.query.filter_by(receiverid=member.id)
    changedstatus = Message.query.filter_by(receiverid=member.id).update({"isread" : True})
    db.session.commit()
    return render_template('home/view_messages.html', receivedmsgs=receivedmsgs, title="Inbox")




#View community broadcast
@home.route('/view_community_broadcast', methods=['GET', 'POST'])
@login_required
def view_community_broadcast():
    """
    View community broadcast messages as long as broadcastall value is 1 for that message
    """

    broadcast = Broadcast.query.filter_by(broadcastall=1)
    return render_template('home/view_community_broadcast.html', broadcast=broadcast, title="Community broadcast")

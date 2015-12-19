from datetime import datetime
from threading import Thread

from flask import Blueprint, current_app, flash, redirect, render_template
from flask import url_for, abort, session as user_session
from flask.ext.mail import Message

from .. import mail
from ..models import Notification, Package
from ..orm import Session
from .prefects import login_required, roles_required


owls_blueprint = Blueprint('owls', __name__, url_prefix='/email')


@owls_blueprint.route('/')
@login_required()
def owls_index():
    return render_template('owls.html')


@owls_blueprint.route('/<int:package_id>/', methods=['POST'])
@login_required()
@roles_required({'employee', 'administrator'})
def send_notification(package_id):
    db_session = Session()

    package = db_session.query(Package).filter_by(id=package_id).one()
    student = package.student

    sender_name = package.sender_name

    notification_count = len(package.notifications) + 1
    email_address = student.account.email_address
    first_name = student.first_name

    notification = Notification(
        package_id=package_id,
        email_address=email_address,
        send_date=datetime.now(),
        send_count=notification_count)

    db_session.add(notification)

    db_session.commit()
    db_session.close()

    send_email(
        email_address,
        'You\'ve got mail.',
        'email/notification',
        package_id=package_id,
        name=first_name,
        notification_count=notification_count,
        sender=sender_name
        )

    flash(
        'Notification email number {} has been sent to student.'.format(
            notification_count
            ), 'success'
        )
    return redirect(url_for('.view_notification', package_id=package_id))


@owls_blueprint.route('/packages/<int:package_id>/')
@login_required()
@roles_required({'student', 'employee', 'administrator'})
def view_notification(package_id):
    if user_session['role'] == 'student':
        return redirect(
            url_for('.view_notification_self', package_id=package_id)
            )
    db_session = Session()
    notifications = db_session.query(
        Notification
        ).filter_by(package_id=package_id).all()
    return render_template('owlery.html', notifications=notifications)


@owls_blueprint.route('/package/me/<int:package_id>/')
@login_required()
@roles_required({'student'})
def view_notification_self(package_id):
    db_session = Session()
    package = db_session.query(
        Package
        ).filter_by(id=package_id).one()
    if user_session['id'] != package.student_id:
        abort(403)
    notifications = db_session.query(
        Notification
        ).filter_by(package_id=package_id).all()
    return render_template('owlery.html', notifications=notifications)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=_send_async_email, args=[app, msg])
    thr.start()
    return thr


def _send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

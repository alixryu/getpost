from datetime import datetime
from threading import Thread

from flask import Blueprint, current_app, flash, redirect, render_template
from flask import url_for
from flask.ext.mail import Message

from .. import mail
from ..models import Notification, Package
from ..orm import Session


owls_blueprint = Blueprint('owls', __name__, url_prefix='/email')


@owls_blueprint.route('/')
def owls_index():
    return render_template('owls.html')


@owls_blueprint.route('/<int:package_id>/', methods=['POST'])
def send_notification(package_id):
    db_session = Session()

    package = db_session.query(Package).filter_by(id=package_id).one()
    student = package.student

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
        notification_count=notification_count)

    flash('Notification email number ' +
          str(notification_count)+'has been sent to student.')
    return redirect(url_for('.view_notification', package_id=package_id))


@owls_blueprint.route('/package/<int:package_id>/')
def view_notification(package_id):
    db_session = Session()
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

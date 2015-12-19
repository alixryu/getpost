from flask import Blueprint, render_template, redirect, session as user_session
from flask import abort, flash, request, url_for

from ..models import Package, Student
from ..orm import Session
from .prefects import login_required, roles_required, user_session_require


parcels_blueprint = Blueprint('parcels', __name__, url_prefix='/packages')


@parcels_blueprint.route('/')
@login_required()
@user_session_require({'role'})
@roles_required({'student', 'employee', 'administrator'})
def parcels_index():
    if user_session['role'] == 'student':
        return redirect('/packages/me/', 303)
    else:
        return render_template('sirius.html')


@parcels_blueprint.route('/me/')
@login_required('/auth/')
@user_session_require({'role'})
@roles_required({'student', 'employee'}, '/packages/')
def parcels_view_self():
    account_id = user_session['id']

    db_session = Session()
    base_query = db_session.query(Package)

    if user_session['role'] == 'student':
        packages = base_query.filter_by(student_id=account_id).all()
        return render_template('parcels_for_wizards.html', packages=packages)
    elif user_session['role'] == 'employee':
        packages = base_query.filter_by(received_by=account_id).all()
        return render_template('parcels.html', packages=packages)
    else:
        abort(404)


@parcels_blueprint.route('/<int:account_id>/')
@login_required()
@user_session_require({'role'})
@roles_required({'employee', 'administrator'})
def parcels_view(account_id):
    db_session = Session()
    packages = db_session.query(
        Package
        ).filter_by(student_id=account_id).all()
    return render_template('parcels.html', packages=packages)


@parcels_blueprint.route('/new', methods=['POST'])
@login_required()
@user_session_require({'role'})
@roles_required({'employee', 'administrator'})
def parcels_create():
    sender_name = request.form['sender_name']
    ocmr = request.form['ocmr']
    arrival_date = request.form['arrival_date']

    db_session = Session()

    student = db_session.query(Student).filter_by(ocmr=ocmr).one()

    package = Package(
        sender_name=sender_name,
        student_id=student.id,
        arrival_date=arrival_date,
        received_by=user_session['id'],
        status='not_picked_up'
        )

    db_session.add(package)

    db_session.commit()
    db_session.close()

    flash('Package has been added for student.', 'success')
    return redirect(url_for('.parcels_view_self'))

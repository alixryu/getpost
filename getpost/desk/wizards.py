from math import ceil

from flask import Blueprint, render_template, request, redirect, flash, abort, session as user_session

from . import ACCOUNT_PER_PAGE as page_size
from ..models import Account, Student
from ..orm import Session
from .prefects import login_required, user_session_require, roles_required, roles_or_match_required, validate_student_field


wizards_blueprint = Blueprint(
    'wizards',
    __name__,
    url_prefix='/students'
)

editable = {
    'student': {'aname', 'email'},
    'employee': {'fname', 'lname', 'tnum', 'aname', 'email'},
    'administrator': {'fname', 'lname', 'tnum', 'aname', 'email'}
}

viewable = {
    'person': {'first_name', 'last_name', 'alternative_name', 'ocmr', 't_number'},
    'account': {'email_address'}
}

@wizards_blueprint.route('/')
@login_required()
@user_session_require({'role'})
def wizards_index():
    if user_session['role'] == 'student':
        return redirect('/students/me/', 303)
    neg_check = lambda x: x if x >= 1 else 1
    page = neg_check(request.args.get('page', 1, type=int))

    db_session = Session()

    base_query = db_session.query(Student)
    page_count = int(ceil(base_query.count()/page_size))

    paginated_students = base_query.limit(
        page_size
    ).offset(
        (page-1)*page_size
    ).from_self().join(Account).all()

    students = []
    for s_a in paginated_students:
        student = {}
        student.update(s_a.as_dict(
            {'first_name', 'last_name', 'alternative_name', 'ocmr', 't_number'}
        ))
        student.update(s_a.account.as_dict(
            {'email_address', 'role', 'verified'}
        ))
        students.append(student)
    db_session.close()
    return render_template(
        'wizards.html', students=students, count=page_count
    )

@wizards_blueprint.route('/me/')
@login_required('/auth/')
@user_session_require({'role'})
@roles_required({'student'}, '/')
def wizards_self():
    return redirect("/students/{}/".format(user_session['id']), 303)

@wizards_blueprint.route('/<int:id>/')
@login_required()
@user_session_require({'role'})
@roles_or_match_required({'employee', 'administrator'})
def wizards_view(id):
    db_session = Session()
    account = db_session.query(Account).get(id)
    if account.role != 'student':
        abort(404)
    student = account.student
    student_dict = {}
    student_dict.update(account.as_dict(viewable['account']))
    student_dict.update(student.as_dict(viewable['person']))
    db_session.close()
    template_editable = editable.get(user_session['role'], set())
    return render_template('transfigure.html', student=student_dict, editable=template_editable)

@wizards_blueprint.route('/<int:id>/edit/', methods={'POST'})
@login_required()
@user_session_require({'role'})
@roles_or_match_required({'employee', 'administrator'})
def wizards_edit(id):
    db_session = Session()
    account = db_session.query(Account).get(id)
    if account.role != 'student':
        abort(404)
    student = account.student
    if student:
        allowed_fields = editable.get(user_session['role'], set())
        requested_fields = set(request.form)
        if requested_fields <= allowed_fields:
            if attempt_update(account, student, request.form):
                flash('Account updated successfully!', 'success')
                db_session.commit()
                db_session.close()
            else:
                db_session.rollback()
                db_session.close()
            return redirect("/students/{}/".format(id), 303)
        else:
            denied_fields = requested_fields - allowed_fields
            flash("Cannot edit the following fields for this student: {}".format(', ').join(denied_fields), 'error')
            return redirect("/students/{}/".format(id), 303)
    else:
        flash('Could locate corresponding student object in database', 'error')
        return redirect('/', 303)

def attempt_update(account, student, form):
    success = True
    updates = {}
    for field, value in form.items():
        if validate_student_field(field, value):
            if field == 'email':
                account.email_address = value
                updates['email_address'] = value
            elif field == 'tnum':
                if value[0] == 'T':
                    value = value[1:]
                student.t_number = value
                updates['t_number'] = value
            elif field == 'fname':
                student.first_name = value
                updates['first_name'] = value
            elif field == 'lname':
                student.last_name = value
                updates['last_name'] = value
            elif field == 'aname':
                student.alternative_name = value
                updates['alternative_name'] = value
        else:
            success = False
    if success:
        user_session.update(updates)
    return success

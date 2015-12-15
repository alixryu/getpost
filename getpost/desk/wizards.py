from math import ceil

from flask import Blueprint, render_template, request, redirect, flash, abort, session as user_session

from . import ACCOUNT_PER_PAGE as page_size
from ..models import Account, Student
from ..orm import Session
from .prefects import login_required, user_session_require, roles_required, roles_or_match_required, validate_field


wizards_blueprint = Blueprint(
    'wizards',
    __name__,
    url_prefix='/students'
)

READ_ONLY = {
    'match': ('first_name', 'last_name', 'ocmr', 't_number'),
    'employee': (),
    'administrator': ()
}

READ_WRITE = {
    'match': ('alternative_name', 'email_address'),
    'employee': ('verified', 'first_name', 'last_name', 'ocmr', 't_number', 'alternative_name', 'email_address'),
    'administrator': ('verified', 'first_name', 'last_name', 'ocmr', 't_number', 'alternative_name', 'email_address')
}

INPUT_FIELDS = {
    'first_name': {
        'type': 'text',
        'title': 'First Name',
        'pattern': "[a-zA-Z '-]+"
    },
    'last_name': {
        'type': 'text',
        'title': 'Last Name',
        'pattern': "[a-zA-Z '-]+"
    },
    'alternative_name': {
        'type': 'text',
        'title': 'Preferred Name',
        'pattern': "[a-zA-Z '-]+"
    },
    'email_address': {
        'type': 'email',
        'title': 'Email Address',
        'pattern': r'.+@.+\..+'
    },
    't_number': {
        'type': 'text',
        'title': 'T number',
        'pattern': 'T?[0-9]{8}'
    },
    'ocmr': {
        'type': 'text',
        'title': 'OCMR number',
        'pattern': '[0-9]{1,4}'
    },
    'verified': {
        'type': 'checkbox',
        'title': 'Verified'
    }
}

def get_read_only(account):
    if account.id == user_session['id']:
        return READ_ONLY['match']
    else:
        return READ_ONLY.get(user_session['role'], [])

def get_read_write(account):
    if account.id == user_session['id']:
        return READ_WRITE['match']
    else:
        return READ_WRITE.get(user_session['role'], [])


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
    if not (account and account.role == 'student'):
        db_session.close()
        abort(404)
    student = account.student
    read, write = get_read_only(account), get_read_write(account)
    fields = INPUT_FIELDS.copy()
    values = {}
    values.update(account.as_dict(read + write))
    values.update(student.as_dict(read + write))
    for name, value in values.items():
        if name in fields:
            if name in read and (value is None or value == ''):
                fields[name]['value'] = 'None listed'
            elif type(value) in {int, str}:
                fields[name]['value'] = value
            elif type(value) == bool:
                if name == 'verified':
                    fields[name]['checked'] = value
                    fields[name]['label'] = True
    db_session.close()
    return render_template(
        'transfigure.html', action='edit/', method='POST', read=read,
        write=write, fields=fields, role='Student'
    )

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
        denied_fields = set(get_read_only(account))
        allowed_fields = set(get_read_write(account))
        requested_fields = set(request.form)
        if not denied_fields.intersection(requested_fields):
            edit_fields = {field: request.form[field] for field in request.form if field in allowed_fields}
            if not edit_fields:
                flash('No update parameters given', 'error')
            else:
                if attempt_update(account, student, edit_fields):
                    flash('Account updated successfully!', 'success')
                    db_session.commit()
                else:
                    db_session.rollback()
            db_session.close()
            return redirect("/students/{}/".format(id), 303)
        else:
            db_session.close()
            flash("Cannot edit the following fields for this students: {}".format(', ').join(denied_fields.intersection(requested_fields)), 'error')
            return redirect("/employee/{}/".format(id), 303)
    else:
        db_session.close()
        flash('Could locate corresponding student object in database', 'error')
        return redirect('/', 303)

def attempt_update(account, student, form):
    success = True
    updates = {}
    for field, value in form.items():
        validated = validate_field(field, value)
        if validated is not None:
            if field == 'email_address':
                account.email_address = validated
                updates['email_address'] = validated
            elif field == 't_number':
                if value[0] == 'T':
                    value = value[1:]
                student.t_number = validated
                updates['t_number'] = validated
            elif field == 'first_name':
                student.first_name = validated
                updates['first_name'] = validated
            elif field == 'last_name':
                student.last_name = validated
                updates['last_name'] = validated
            elif field == 'alternative_name':
                student.alternative_name = validated
                updates['alternative_name'] = validated
            else:
                flash("Cannot update {} field".format(field), 'error')
                success = False
        else:
            success = False
    if success and user_session['id'] == account.id:
        user_session.update(updates)
    return success

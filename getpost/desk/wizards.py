from math import ceil
from copy import deepcopy

from flask import Blueprint, render_template, request, redirect, session as user_session

from . import ACCOUNT_PER_PAGE as page_size
from ..models import Account, Student
from ..orm import Session
from .prefects import login_required, roles_required, roles_or_match_required, user_session_require
from .transfigure import view_user, edit_user

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

def get_read_only(id):
    if id == user_session['id'] and 'match' in READ_ONLY:
        return READ_ONLY['match']
    else:
        return READ_ONLY.get(user_session['role'], [])

def get_read_write(id):
    if id == user_session['id'] and 'match' in READ_WRITE:
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
@roles_required({'student'})
def wizards_self():
    return redirect("/students/{}/".format(user_session['id']), 303)

@wizards_blueprint.route('/<int:id>/')
@login_required()
@roles_or_match_required({'employee', 'administrator'})
def wizards_view(id):
    read, write = get_read_only(id), get_read_write(id)
    fields = deepcopy(INPUT_FIELDS)
    return view_user(id, 'student', read, write, fields)

@wizards_blueprint.route('/<int:id>/edit/', methods={'POST'})
@login_required()
@roles_or_match_required({'employee', 'administrator'})
def wizards_edit(id):
    read, write = get_read_only(id), get_read_write(id)
    return edit_user(id, 'student', read, write, request.form)

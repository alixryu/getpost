from math import ceil
from copy import deepcopy

from flask import Blueprint, render_template, request, redirect, session as user_session

from . import ACCOUNT_PER_PAGE as page_size
from ..models import Account, Employee
from ..orm import Session
from .prefects import login_required, roles_required, roles_or_match_required
from .transfigure import view_user, edit_user


professors_blueprint = Blueprint(
    'professors',
    __name__,
    url_prefix='/employees'
)

READ_ONLY = {
    'match': (),
    'employee': ('verified', 'first_name', 'last_name', 'email_address'),
    'administrator': ()
}

READ_WRITE = {
    'match': ('first_name', 'last_name', 'email_address'),
    'employee': (),
    'administrator': ('verified', 'first_name', 'last_name', 'email_address')
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
    'email_address': {
        'type': 'email',
        'title': 'Email Address',
        'pattern': r'.+@.+\..+'
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


@professors_blueprint.route('/')
@login_required()
@roles_required({'employee', 'administrator'})
def professors_index():
    if user_session['role'] == 'employee':
        return redirect('/employee/me/', 303)
    neg_check = lambda x: x if x >= 1 else 1
    page = neg_check(request.args.get('page', 1, type=int))

    session = Session()

    base_query = session.query(Employee)
    page_count = int(ceil(base_query.count()/page_size))

    paginated_employees = base_query.limit(
        page_size
    ).offset(
        (page-1)*page_size
    ).from_self().join(Account).all()

    employees = []
    for e_a in paginated_employees:
        employee = {}
        employee['email_address'] = e_a.account.email_address
        employee['role'] = e_a.account.role
        employee['verified'] = e_a.account.verified
        employee['first_name'] = e_a.first_name
        employee['last_name'] = e_a.last_name
        employees.append(employee)
    session.close()
    return render_template(
        'professors.html', employees=employees, count=page_count
    )

@professors_blueprint.route('/me/')
@login_required('/auth/')
@roles_required({'employee'})
def professors_self():
    return redirect("/employees/{}/".format(user_session['id']), 303)

@professors_blueprint.route('/<int:id>/')
@login_required()
@roles_required({'employee', 'administrator'})
def professors_view(id):
    read, write = get_read_only(id), get_read_write(id)
    fields = deepcopy(INPUT_FIELDS)
    return view_user(id, 'employee', read, write, fields)

@professors_blueprint.route('/<int:id>/edit/', methods={'POST'})
@login_required()
@roles_or_match_required({'administrator'})
def professors_edit(id):
    read, write = get_read_only(id), get_read_write(id)
    return edit_user(id, 'employee', read, write, request.form)

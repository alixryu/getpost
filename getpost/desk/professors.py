from math import ceil
from copy import deepcopy

from flask import Blueprint, render_template, request, redirect, flash, abort, session as user_session

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
    'match': ('verified',),
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
    if id == user_session['id']:
        return READ_ONLY['match']
    else:
        return READ_ONLY.get(user_session['role'], [])

def get_read_write(id):
    if id == user_session['id']:
        return READ_WRITE['match']
    else:
        return READ_WRITE.get(user_session['role'], [])


@professors_blueprint.route('/')
@login_required()
@roles_required({'employee', 'administrator'})
def professors_index():
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
@roles_required({'employee'}, '/')
def professors_self():
    return redirect("/employees/{}/".format(user_session['id']), 303)

@professors_blueprint.route('/<int:id>/')
@login_required()
@roles_required({'employee', 'administrator'})
def professors_view(id):
    read, write = get_read_only(id), get_read_write(id)
    fields = deepcopy(INPUT_FIELDS)
    return view_user(id, 'employee', read, write, fields)
    # db_session = Session()
    # account = db_session.query(Account).get(id)
    # if not (account and account.role == 'employee'):
    #     db_session.close()
    #     abort(404)
    # employee = account.employee
    # read, write = get_read_only(account), get_read_write(account)
    # values = {}
    # values.update(account.as_dict(read + write))
    # values.update(employee.as_dict(read + write))
    # fields = INPUT_FIELDS.copy()
    # for name, value in values.items():
    #     if name in fields:
    #         if name in read and (value is None or value == ''):
    #             fields[name]['value'] = 'None listed'
    #         elif type(value) in {str, int}:
    #             fields[name]['value'] = value
    #         elif type(value) == bool:
    #             if name == 'verified':
    #                 fields[name]['checked'] = value
    #                 fields[name]['label'] = True
    # db_session.close()
    # return render_template(
    #     'transfigure.html', action='edit/', method='POST', read=read,
    #     write=write, fields=fields, role='Employee'
    # )

@professors_blueprint.route('/<int:id>/edit/', methods={'POST'})
@login_required()
@roles_or_match_required({'administrator'})
def professors_edit(id):
    read, write = get_read_only(id), get_read_write(id)
    return edit_user(id, 'employee', read, write, request.form)
#     db_session = Session()
#     account = db_session.query(Account).get(id)
#     if account.role != 'employee':
#         abort(404)
#     employee = account.employee
#     if employee:
#         denied_fields = set(get_read_only(account))
#         allowed_fields = set(get_read_write(account))
#         requested_fields = set(request.form)
#         if not denied_fields.intersection(requested_fields):
#             edit_fields = {field: request.form[field] for field in request.form if field in allowed_fields}
#             if attempt_update(account, employee, edit_fields):
#                 flash('Account updated successfully!', 'success')
#                 db_session.commit()
#             else:
#                 db_session.close()
#             db_session.rollback()
#             return redirect("/employees/{}/".format(id), 303)
#         else:
#             db_session.close()
#             flash("Cannot edit the following fields for this employee: {}".format(', ').join(denied_fields.intersection(requested_fields)), 'error')
#             return redirect("/employee/{}/".format(id), 303)
#     else:
#         db_session.close()
#         flash('Could locate corresponding employee object in database', 'error')
#         return redirect('/', 303)
#
# def attempt_update(account, employee, form):
#     success = True
#     updates = {}
#     for field, value in form.items():
#         validated = validate_field(field, value)
#         if validated is not None:
#             if field == 'email_address':
#                 account.email_address = validated
#                 updates['email_address'] = validated
#             elif field == 'first_name':
#                 employee.first_name = validated
#                 updates['first_name'] = validated
#             elif field == 'last_name':
#                 employee.last_name = validated
#                 updates['last_name'] = validated
#             else:
#                 print("Unrecognized field: {}".format(field))
#         else:
#             success = False
#     if success and user_session['id'] == account.id:
#         user_session.update(updates)
#     return success

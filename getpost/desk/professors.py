from math import ceil

from flask import Blueprint, render_template, request

from . import ACCOUNT_PER_PAGE as page_size
from ..models import Account, Employee
from ..orm import Session


professors_blueprint = Blueprint(
    'professors',
    __name__,
    url_prefix='/employees'
)


@professors_blueprint.route('/')
@professors_blueprint.route('/view/')
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


@professors_blueprint.route('/view/all/')
def professors_all():
    return render_template('professors.html')


@professors_blueprint.route('/view/me/')
def professors_user():
    return render_template('professors.html')

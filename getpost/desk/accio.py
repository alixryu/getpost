from math import ceil

from flask import Blueprint, render_template, request, redirect, flash, abort, session as user_session

from . import ACCOUNT_PER_PAGE as page_size
from ..models import Account, Student
from ..orm import Session
from .prefects import login_required, user_session_require, roles_required, roles_or_match_required, validate_field


accio_blueprint = Blueprint(
    'accio',
    __name__,
    url_prefix='/results'
)


@accio_blueprint.route('/')
@login_required()
@user_session_require({'role'})
def accio_index():

    if user_session['role'] == 'student':
        return redirect('/students/me/', 303)
    neg_check = lambda x: x if x >= 1 else 1
    page = neg_check(request.args.get('page', 1, type=int))

    search_params = {}
    search_params['firstname'] = request.args.get('firstname', '', type=str)
    search_params['lastname'] = request.args.get('lastname', '', type=str)
    search_params['preferredname'] = request.args.get('preferredname', '', type=str)
    search_params['ocmr'] = request.args.get('ocmr', '', type=str)
    search_params['tnumber'] = request.args.get('tnumber', '', type=str)

    search_params = {key: value for (key, value) in search_params.items() if value != ''}
    db_session = Session()

    base_query = db_session.query(Student)

    #for param, val in search_params.items():

        #base_query.filter(Student.param == val)

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

    return render_template('accio.html', search_params=search_params, students=students)
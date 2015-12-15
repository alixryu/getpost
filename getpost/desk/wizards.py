from math import ceil

from flask import Blueprint, render_template, request

from . import ACCOUNT_PER_PAGE as page_size
from ..models import Account, Student
from ..orm import Session


wizards_blueprint = Blueprint(
    'wizards',
    __name__,
    url_prefix='/students'
)


@wizards_blueprint.route('/')
def wizards_index():
    neg_check = lambda x: x if x >= 1 else 1
    page = neg_check(request.args.get('page', 1, type=int))

    session = Session()

    base_query = session.query(Student)
    page_count = int(ceil(base_query.count()/page_size))

    paginated_students = base_query.limit(
        page_size
    ).offset(
        (page-1)*page_size
    ).from_self().join(Account).all()

    students = []
    for s_a in paginated_students:
        student = {}
        student['email_address'] = s_a.account.email_address
        student['role'] = s_a.account.role
        student['verified'] = s_a.account.verified
        student['first_name'] = s_a.first_name
        student['last_name'] = s_a.last_name
        student['alternative_name'] = s_a.alternative_name
        student['ocmr'] = s_a.ocmr
        student['t_number'] = s_a.t_number
        students.append(student)
    session.close()
    return render_template(
        'wizards.html', students=students, count=page_count
    )

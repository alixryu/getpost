from math import ceil
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, render_template, request, redirect, flash, session as user_session

from . import ACCOUNT_PER_PAGE as page_size
from ..models import Account, Student, Employee
from ..orm import ManagedSession
from .prefects import login_required, roles_required


accio_blueprint = Blueprint(
    'accio',
    __name__,
    url_prefix='/results'
)


def search_user(role, form):
    neg_check = lambda x: x if x >= 1 else 1
    page = neg_check(request.args.get('page', 1, type=int))

    with ManagedSession(False) as db_session:
        if role == 'student':
            searchpage = '/students/'
            query_class = Student
            valid_params = {'firstname': 'First Name', 'lastname': 'Last Name', 'preferredname': 'Preferred Name', 'ocmr': 'OCMR number', 'tnumber': 'T number'}
            object_translations = {'first_name': 'First Name', 'last_name': 'Last Name', 'alternative_name': 'Preferred Name', 'ocmr': 'OCMR number', 't_number': 'T number'}
        elif role == 'employee':
            searchpage = '/employees/'
            query_class = Employee
            valid_params = {'firstname': 'First Name', 'lastname': 'Last Name'}
            object_translations = {'first_name': 'First Name', 'last_name': 'Last Name'}
        else:
            flash("Unrecognized search role: {}".format(role), 'error')
            return redirect('')
        parameters = {valid_params[param]: form[param] for param in form if param in valid_params}
        base_query = db_session.query(query_class)
        noparams = True

        for param, value in parameters.items():
            if value:
                if param == 'First Name':
                    base_query = base_query.filter(query_class.first_name == value)
                elif param == 'Last Name':
                    base_query = base_query.filter(query_class.last_name == value)
                elif param == 'Preferred Name':
                    base_query = base_query.filter(query_class.alternative_name == value)
                elif param == 'OCMR number':
                    base_query = base_query.filter(query_class.ocmr == value)
                elif param == 'T number':
                    base_query = base_query.filter(query_class.t_number == value)
                noparams = False

        page_count = int(ceil(base_query.count() / page_size))
        paginated_students = base_query.limit(
            page_size
            ).offset(
            (page-1)*page_size
            ).from_self().join(Account).all()

        results = []
        for s_a in paginated_students:
            result = {}
            result.update({object_translations[key]: value for key, value in s_a.as_dict(
                {'first_name', 'last_name', 'alternative_name', 'ocmr', 't_number'}
            ).items()})
            result['id'] = s_a.id
            if 'OCMR number' in result and result['OCMR number'] == '-1':
                result['OCMR number'] = None
            results.append(result)

        return render_template('accio.html', parameters=parameters, role=role, results=results, noparams=noparams, searchpage=searchpage)

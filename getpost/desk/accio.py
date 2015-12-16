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

	search_params = {}
	search_params['firstname'] = request.args.get('firstname', '', type=str)
	search_params['lastname'] = request.args.get('lastname', '', type=str)
	search_params['preferredname'] = request.args.get('preferredname', '', type=str)
	search_params['ocmr'] = request.args.get('ocmr', '', type=str)
	search_params['tnumber'] = request.args.get('tnumber', '', type=str)

	

	return render_template(
        'accio.html', 
        firstname=search_params['firstname'], 
        lastname=search_params['lastname'], 
        preferredname=search_params['preferredname'], 
        ocmr=search_params['ocmr'], 
        tnumber=search_params['tnumber']
    )
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
def accio_index():

    return render_template(
        'accio.html'
    )
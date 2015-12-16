from flask import Blueprint, render_template, redirect, session as user_session

from .prefects import login_required, roles_required, roles_or_match_required, user_session_require


parcels_blueprint = Blueprint('parcels', __name__, url_prefix='/packages')


@parcels_blueprint.route('/')
@login_required()
@user_session_require({'role'})
def parcels_index():
    if user_session['role'] == 'student':
        return redirect('/packages/me/', 303)
    else:
        return render_template('parcels.html')

@parcels_blueprint.route('/me/')
@login_required()
@user_session_require({'role'})
@roles_required({'student'}, '/packages/')
def parcels_self():
    return redirect("/packages/{}/".format(user_session['id']), 303)

@parcels_blueprint.route('/<int:id>/')
@login_required()
@user_session_require({'role'})
@roles_or_match_required({'employee', 'administrator'})
def parcels_view(id):
    return render_template('parcels.html')

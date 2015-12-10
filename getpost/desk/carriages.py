from flask import Blueprint, render_template, session, redirect


carriages_blueprint = Blueprint('carriages', __name__, url_prefix='/login')


@carriages_blueprint.route('/')
def carriages_index():
    return render_template('carriages.html')

@carriages_blueprint.route('/out')
def carriages_out():
    session.pop('logged_in', None)
    return redirect('/', 303)

from flask import Blueprint, render_template


headmaster_blueprint = Blueprint('headmaster', __name__, url_prefix='/admin')


@headmaster_blueprint.route('/')
@headmaster_blueprint.route('/view/')
def headmaster_index():
    return render_template('headmaster.html')

@headmaster_blueprint.route('/view/all/')
def headmaster_all():
    return render_template('headmaster.html')

@headmaster_blueprint.route('/view/me/')
def headmaster_user():
    return render_template('transfigure.html')

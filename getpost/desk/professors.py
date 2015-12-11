from flask import Blueprint, render_template


professors_blueprint = Blueprint('professors', __name__, url_prefix='/employees')


@professors_blueprint.route('/')
@professors_blueprint.route('/view/')
def professors_index():
    return render_template('professors.html')

@professors_blueprint.route('/view/all/')
def professors_all():
    return render_template('professors.html')

@professors_blueprint.route('/view/me/')
def professors_user():
    return render_template('professors.html')

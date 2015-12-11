from flask import Blueprint, render_template, session, redirect, flash


wizards_blueprint = Blueprint('wizards', __name__, url_prefix='/students')


@wizards_blueprint.route('/')
@wizards_blueprint.route('/view/')
def wizards_index():
    return render_template('wizards.html')

@wizards_blueprint.route('/view/all/')
def wizards_all():
    return render_template('wizards.html')

@wizards_blueprint.route('/view/me/')
def wizards_user():
    return render_template('wizards.html')

from flask import Blueprint, render_template


wizards_blueprint = Blueprint('wizards', __name__, url_prefix='/students')


@wizards_blueprint.route('/')
def wizards_index():
    return render_template('wizards.html')

from flask import Blueprint, render_template


boats_blueprint = Blueprint('boats', __name__, url_prefix='/signup')


@boats_blueprint.route('/')
def boats_index():
    return render_template('boats.html')

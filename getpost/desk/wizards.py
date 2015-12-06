from flask import Blueprint


wizards_blueprint = Blueprint('wizards', __name__, url_prefix='/students')


@wizards_blueprint.route('/')
def wizards_index():
    return '<h1>Welcome to the Student Search Page.</h1>'

from flask import Blueprint


lobby_blueprint = Blueprint('lobby', __name__, url_prefix='/lobby')


@lobby_blueprint.route('/')
def lobby_index():
    return '<h1>Welcome to the Firelands lobby.</h1>'

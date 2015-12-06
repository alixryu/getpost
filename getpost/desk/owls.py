from flask import Blueprint


owls_blueprint = Blueprint('owls', __name__, url_prefix='/email')


@owls_blueprint.route('/')
def owls_index():
    return '<h1>Welcome to the Email Management Page.</h1>'

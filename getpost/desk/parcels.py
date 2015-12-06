from flask import Blueprint


parcels_blueprint = Blueprint('parcels', __name__, url_prefix='/packages')


@parcels_blueprint.route('/')
def parcels_index():
    return '<h1>Welcome to the Package Management Page.</h1>'

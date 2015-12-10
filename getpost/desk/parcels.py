from flask import Blueprint, render_template


parcels_blueprint = Blueprint('parcels', __name__, url_prefix='/packages')


@parcels_blueprint.route('/')
def parcels_index():
    return render_template('parcels.html')

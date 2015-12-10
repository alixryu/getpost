from flask import Blueprint, render_template


carriages_blueprint = Blueprint('carriages', __name__, url_prefix='/login')


@carriages_blueprint.route('/')
def carriages_index():
    return render_template('carriages.html')

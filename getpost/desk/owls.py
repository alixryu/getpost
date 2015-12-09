from flask import Blueprint, render_template


owls_blueprint = Blueprint('owls', __name__, url_prefix='/email')


@owls_blueprint.route('/')
def owls_index():
    return render_template('owls.html')

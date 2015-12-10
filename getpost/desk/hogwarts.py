from flask import Blueprint, render_template


hogwarts_blueprint = Blueprint('hogwarts', __name__, url_prefix='')


@hogwarts_blueprint.route('/')
def hogwargs_index():
    return render_template('hogwarts.html')

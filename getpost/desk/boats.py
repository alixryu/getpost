from flask import Blueprint, render_template, redirect


boats_blueprint = Blueprint('boats', __name__, url_prefix='/signup')


@boats_blueprint.route('/')
def boats_index():
    return render_template('boats.html')


@boats_blueprint.route('/new', methods={'POST'})
def boats_new():
    return redirect('/', 303)

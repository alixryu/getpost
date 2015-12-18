from flask import Blueprint, render_template, redirect

from random import randrange


hogwarts_blueprint = Blueprint('hogwarts', __name__, url_prefix='')


@hogwarts_blueprint.route('/')
def hogwargs_index():
    if not randrange(100):
        return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    return render_template('hogwarts.html')

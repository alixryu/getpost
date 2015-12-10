from flask import Blueprint, render_template, redirect, url_for


hogwarts_blueprint = Blueprint('hogwarts', __name__, url_prefix='')

css_specials = {'template.css': 'maraudersmap.css',
                'home.css': 'hogwarts.css',
                'signup.css': 'boats.css'}
js_specials = {'signup.js': 'boats.js'}


@hogwarts_blueprint.app_errorhandler(500)
def internal(error):
    desc = 'Uh oh! Something went wrong.'
    return render_template(
        'voldemort.html', status=500, description=desc
    ), 500


@hogwarts_blueprint.app_errorhandler(404)
def not_found(error):
    desc = 'This page does not exist.'
    return render_template(
        'voldemort.html', status=404, description=desc
    ), 404


@hogwarts_blueprint.route('/')
def hogwargs_index():
    return render_template('hogwarts.html')


@hogwarts_blueprint.route('/css/<path:path>')
def send_css(path):
    if path in css_specials:
        path = 'css/'+css_specials[path]
    return redirect(url_for('static', filename=path))


@hogwarts_blueprint.route('/js/<path:path>')
def send_js(path):
    if path in js_specials:
        path = 'js/'+js_specials[path]
    return redirect(url_for('static', filename=path))

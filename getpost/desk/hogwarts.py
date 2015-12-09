from flask import Blueprint, render_template, send_from_directory


hogwarts_blueprint = Blueprint('hogwarts', __name__, url_prefix='')

css_specials = {'template.css': 'maraudersmap.css'}
js_specials = {}


@hogwarts_blueprint.route('/')
def hogwargs_index():
    return render_template('maraudersmap.html')

@hogwarts_blueprint.route('/css/<path:path>')
def send_css(path):
    if path in css_specials:
        path = css_specials[path]
    return send_from_directory('styles', path)

@hogwarts_blueprint.route('/js/<path:path>')
def send_js(path):
    if path in js_specials:
        path = js_specials[path]
    return send_from_directory('scripts', path)
